import socket
from pathlib import Path

import pandas as pd


NAO_ENCONTRADO = "host não encontrado"


def reverse_lookup(ip: str) -> str:
    ip = (ip or "").strip()
    if not ip:
        return NAO_ENCONTRADO

    try:
        hostname, aliases, _ = socket.gethostbyaddr(ip)
        hosts = []
        for h in [hostname, *aliases]:
            h = (h or "").strip().rstrip(".")
            if h and h not in hosts:
                hosts.append(h)

        return ", ".join(hosts) if hosts else NAO_ENCONTRADO

    except (socket.herror, socket.gaierror, TimeoutError, OSError):
        return NAO_ENCONTRADO


def main():
    input_path = Path(input("Sheet path: ").strip())
    sheet_name = "IPs"

    df = pd.read_excel(input_path, sheet_name=sheet_name)

    if "IPs" not in df.columns:
        raise SystemExit("Erro: a planilha precisa ter uma coluna chamada exatamente 'IPs'.")
    
    df["Hosts"] = df["IPs"].astype(str).apply(reverse_lookup)

    output_path = input_path.with_name(f"{input_path.stem}_com_hosts{input_path.suffix}")
    df.to_excel(output_path, index=False)

    print(f"OK: arquivo gerado em: {output_path.resolve()}")


if __name__ == "__main__":
    try:
        socket.setdefaulttimeout(3.0)
    except Exception:
        pass

    main()