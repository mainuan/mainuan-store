#!/usr/bin/python3
"""Programa auxiliar da Mainuan Store (corre como root via pkexec).

Modos:
  helper.py apt <ficheiro-cancelar> <argumentos apt-get>      (instalar/remover/atualizar com cancelamento)
  helper.py flatpak <ficheiro-cancelar> <argumentos flatpak>  (instalação system-wide com palavra-passe)
  helper.py <ficheiro> <índice> <yes|no>                      (ativar/desativar fonte APT)

Só aceita argumentos de uma lista restrita; recusa tudo o resto."""
import os
import re
import signal
import subprocess
import sys

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9+._:~-]*$")
APT_SUB = {"install", "remove", "update", "upgrade"}
APT_FLAGS = {"-y", "--only-upgrade"}
APT_OPT_VALUES = {"APT::Status-Fd=1", "Dpkg::Use-Pty=0"}
FLATPAK_SUB = {"install", "uninstall", "update"}
FLATPAK_FLAGS = {"--system", "-y", "--noninteractive", "--appstream"}


def toggle_sources(text, idx, flag):
    stanzas = re.split(r"\n\s*\n", text.strip("\n"))
    lines = [l for l in stanzas[idx].split("\n") if not l.lower().startswith("enabled:")]
    lines.append("Enabled: " + flag)
    stanzas[idx] = "\n".join(lines)
    return "\n\n".join(stanzas) + "\n"


def toggle_list(text, idx, flag):
    lines = text.split("\n")
    m = re.match(r"^(\s*)(#\s*)?(deb\s+.*)$", lines[idx])
    if not m:
        raise ValueError("linha inválida")
    lines[idx] = m.group(1) + ("" if flag == "yes" else "# ") + m.group(3)
    return "\n".join(lines)


def valid_apt(args):
    i = 0
    while i < len(args) and args[i] == "-o":
        if i + 1 >= len(args) or args[i + 1] not in APT_OPT_VALUES:
            return False
        i += 2
    if i >= len(args) or args[i] not in APT_SUB:
        return False
    for a in args[i + 1:]:
        if a in APT_FLAGS or NAME_RE.match(a):
            continue
        if a.startswith("/") and a.endswith(".deb") and "\0" not in a and os.path.isfile(a):
            continue
        return False
    return True


def valid_flatpak(args):
    if not args or args[0] not in FLATPAK_SUB:
        return False
    return all(a in FLATPAK_FLAGS or NAME_RE.match(a) for a in args[1:])


def valid_cancel(path):
    return (os.path.basename(path).startswith("cancel-")
            and os.path.dirname(path).endswith("/.cache/mainuan-store")
            and not os.path.islink(path))


def run_guarded(prog, args, cancel):
    env = {"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "DEBIAN_FRONTEND": "noninteractive",
           "HOME": "/root", "LANG": "C.UTF-8"}
    p = subprocess.Popen([prog] + args, env=env)
    while True:
        try:
            return p.wait(timeout=0.3)
        except subprocess.TimeoutExpired:
            pass
        if os.path.exists(cancel):
            p.send_signal(signal.SIGINT)
            try:
                p.wait(timeout=20)
            except subprocess.TimeoutExpired:
                p.terminate()
                p.wait(timeout=10)
            return 130


def toggle_main(argv):
    if len(argv) != 3:
        return 2
    path, flag = argv[0], argv[2]
    real = os.path.realpath(path)
    allowed = real == "/etc/apt/sources.list" or (
        real.startswith("/etc/apt/sources.list.d/") and real.endswith((".list", ".sources")))
    if not allowed or flag not in ("yes", "no"):
        return 2
    try:
        idx = int(argv[1])
        with open(real, encoding="utf-8") as f:
            text = f.read()
        new = toggle_sources(text, idx, flag) if real.endswith(".sources") else toggle_list(text, idx, flag)
        tmp = real + ".mainuan-tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(new)
        os.chmod(tmp, 0o644)
        os.replace(tmp, real)
    except Exception as exc:  # noqa: BLE001
        print(exc, file=sys.stderr)
        return 1
    return 0


def main():
    argv = sys.argv[1:]
    if argv and argv[0] in ("apt", "flatpak"):
        if len(argv) < 3 or not valid_cancel(argv[1]):
            return 2
        args = argv[2:]
        if argv[0] == "apt":
            return run_guarded("/usr/bin/apt-get", args, argv[1]) if valid_apt(args) else 2
        return run_guarded("/usr/bin/flatpak", args, argv[1]) if valid_flatpak(args) else 2
    return toggle_main(argv)


if __name__ == "__main__":
    sys.exit(main())
