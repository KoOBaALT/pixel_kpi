import argparse
from pixel_kpi.displays.pixoo_display import PixooDisplay
from pixel_kpi.displays.terminal_display import TerminalDisplay
from pixel_kpi.displays.matplotlib_display import MatplotlibDisplay
from pixel_kpi.views.notion_sprint_view import NotionSprintView
from pixel_kpi.connectors.notion_connector import NotionConnector
from pixel_kpi.processors.notion.sprint_processor import SprintProcessor
from pixel_kpi.connectors.github_connector import GithubConnector
from pixel_kpi.processors.github.star_processor import StarProcessor
from pixel_kpi.views.github_stars_view import GithubStarsView
from pixel_kpi.views.rotating_view import RotatingView
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Display GitHub stars and Notion sprint data on Pixoo display.")
    parser.add_argument('--display_type', required=True, choices=['pixoo', 'matplot', 'terminal'], help='Type of display to use')
    parser.add_argument('--ip_address', required=True, help='IP address of the Pixoo display')
    parser.add_argument('--github_api_key', required=True, help='GitHub API key')
    parser.add_argument('--github_repo', required=True, help='GitHub repository in format owner/repo')
    parser.add_argument('--refresh_rate', type=int, default=900, help='Refresh rate in seconds (default: 900)')

    args = parser.parse_args()

    if args.display_type == 'pixoo' and not args.ip_address:
        parser.error("--ip_address is required when display_type is pixoo")

    if args.display_type == 'pixoo':
        display = PixooDisplay(display_name="PixooDisplay", display_id=0, width=64, height=64, ip_address=args.ip_address, simulated=False)
    elif args.display_type == 'terminal':
        display = TerminalDisplay(display_name="TerminalDisplay", display_id=0, width=64, height=64)
    elif args.display_type == 'matplot':
        display = MatplotlibDisplay(display_name="MatplotlibDisplay", display_id=0, width=64, height=64)

    github_connector = GithubConnector(api_key=args.github_api_key)
    star_processor = StarProcessor()

    github_stars_view = GithubStarsView(
        display=display,
        connector=github_connector,
        processor=star_processor,
        refresh_rate=args.refresh_rate,
        main_color=(80, 255, 255),
        repository=args.github_repo
    )

    github_stars_view.run()

if __name__ == "__main__":
    main()

#python examples/github_star_stats.py \
#  --display_type terminal \
#  --github_api_key "your_github_api_key" \
#  --github_repo "owner/repo" \
#  --refresh_rate 900 \
#  --switch_interval 300