import argparse
from pixel_kpi.displays.pixoo_display import PixooDisplay
from pixel_kpi.displays.terminal_display import TerminalDisplay
from pixel_kpi.displays.matplotlib_display import MatplotlibDisplay
from pixel_kpi.views.notion_sprint_view import NotionSprintView
from pixel_kpi.connectors.notion_connector import NotionConnector
from pixel_kpi.processors.notion.sprint_processor import SprintProcessor
import logging

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Display Notion sprint data on Pixoo display.")
    parser.add_argument('--display_type', required=True, choices=['pixoo', 'matplot', 'terminal'], help='Type of display to use')
    parser.add_argument('--ip_address', required=True, help='IP address of the Pixoo display')
    parser.add_argument('--notion_api_key', required=True, help='Notion API key')
    parser.add_argument('--notion_database_id', required=True, help='Notion database ID')
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



    notion_connector = NotionConnector(
        api_key=args.notion_api_key,
        database_id=args.notion_database_id
    )
    
    notion_sprint_processor = SprintProcessor()

    notion_sprint_view = NotionSprintView(
        display=display,
        connector=notion_connector,
        processor=notion_sprint_processor,
        refresh_rate=args.refresh_rate,
        main_color=(80, 255, 255)
    )

    notion_sprint_view.run()

if __name__ == "__main__":
    main()

#python examples/notion_sprint.py \
#  --display_type pixoo \
#  --ip_address "192.168.178.153" \
#  --notion_api_key "your_notion_api_key" \
#  --notion_database_id "your_database_id" \
#  --refresh_rate 900