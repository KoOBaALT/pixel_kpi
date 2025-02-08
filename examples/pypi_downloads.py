import argparse
from pixel_kpi.displays.pixoo_display import PixooDisplay
from pixel_kpi.displays.terminal_display import TerminalDisplay
from pixel_kpi.displays.matplotlib_display import MatplotlibDisplay
from pixel_kpi.connectors.pypi_connector import PyPiConnector
from pixel_kpi.views.package_download_view import PackageDownloadView
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Display PyPi package downloads on different display types.")
    parser.add_argument('--display_type', choices=['pixoo', 'terminal', 'matplot'], required=True, help='Type of display to use')
    parser.add_argument('--package_name', required=True, help='Name of the PyPi package')
    parser.add_argument('--ip_address', help='IP address for Pixoo display (required if display_type is pixoo)')

    args = parser.parse_args()

    if args.display_type == 'pixoo' and not args.ip_address:
        parser.error("--ip_address is required when display_type is pixoo")

    if args.display_type == 'pixoo':
        display = PixooDisplay(display_name="PixooDisplay", display_id=0, width=64, height=64, ip_address=args.ip_address, simulated=False)
    elif args.display_type == 'terminal':
        display = TerminalDisplay(display_name="TerminalDisplay", display_id=0, width=64, height=64)
    elif args.display_type == 'matplot':
        display = MatplotlibDisplay(display_name="MatplotlibDisplay", display_id=0, width=64, height=64)

    pypi_connector = PyPiConnector()

    package_download_view = PackageDownloadView(display=display, connector=pypi_connector, processor=None, refresh_rate=60*15, main_color=(80, 255, 255), package_name=args.package_name)

    package_download_view.run()

if __name__ == "__main__":
    main()

# python examples/pypi_downloads.py --display_type matplot --package_name pi_optimal