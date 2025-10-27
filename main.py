import argparse
from orchestrator.orchestrator import Orchestrator
from utils.logger import get_logger
from dotenv import load_dotenv

logger = get_logger("main")

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Multi-agent Orchestrator")
    parser.add_argument("--topic", "-t", help="Topic to research and write about")
    args = parser.parse_args()

    if not args.topic:
        logger.error("Please provide a topic using --topic")
        return

    orch = Orchestrator()
    result = orch.run(args.topic)
    logger.info("Finished. Outputs saved in: %s", result.get("out_dir"))

if __name__ == "__main__":
    main()
