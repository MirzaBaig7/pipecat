import logging
import sys
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sphinx-build")

# Add source directory to path
docs_dir = Path(__file__).parent
project_root = docs_dir.parent.parent
sys.path.insert(0, str(project_root / "src"))

# Project information
project = "pipecat-ai"
current_year = datetime.now().year
copyright = f"2024-{current_year}, Daily" if current_year > 2024 else "2024, Daily"
author = "Daily"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False

# AutoDoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "exclude-members": "__weakref__,__init__",
    "no-index": True,
    "show-inheritance": True,
}

# Mock imports for optional dependencies
autodoc_mock_imports = [
    "riva",
    "livekit",
    "pyht",  # Base PlayHT package
    "pyht.async_client",  # PlayHT specific imports
    "pyht.client",
    "pyht.protos",
    "pyht.protos.api_pb2",
    "pipecat_ai_playht",  # PlayHT wrapper
    "aiortc",
    "aiortc.mediastreams",
    "cv2",
    "av",
    "pyneuphonic",
    "mem0",
    "mlx_whisper",
    "anthropic",
    "assemblyai",
    "boto3",
    "azure",
    "cartesia",
    "deepgram",
    "elevenlabs",
    "fal",
    "gladia",
    "google",
    "krisp",
    "langchain",
    "lmnt",
    "noisereduce",
    "openai",
    "openpipe",
    "simli",
    "soundfile",
    "pipecat_ai_krisp",
    "pyaudio",
    "_tkinter",
    "tkinter",
    "daily",
    "daily_python",
    "pydantic.BaseModel",
    "pydantic.Field",
    "pydantic._internal._model_construction",
    "pydantic._internal._fields",
    # Moondream dependencies
    "torch",
    "transformers",
    "intel_extension_for_pytorch",
    # Ultravox dependencies
    "huggingface_hub",
    "vllm",
    "vllm.engine.arg_utils",
    "transformers.AutoTokenizer",
    # Langchain dependencies
    "langchain_core",
    "langchain_core.messages",
    "langchain_core.runnables",
    "langchain_core.messages.AIMessageChunk",
    "langchain_core.runnables.Runnable",
    # LiveKit dependencies
    "livekit",
    "livekit.rtc",
    "livekit_api",
    "livekit_protocol",
    "tenacity",
    "tenacity.retry",
    "tenacity.stop_after_attempt",
    "tenacity.wait_exponential",
    "rtc",
    "rtc.Room",
    "rtc.RoomOptions",
    "rtc.AudioSource",
    "rtc.LocalAudioTrack",
    "rtc.TrackPublishOptions",
    "rtc.TrackSource",
    "rtc.AudioStream",
    "rtc.AudioFrameEvent",
    "rtc.AudioFrame",
    "rtc.Track",
    "rtc.TrackKind",
    "rtc.RemoteParticipant",
    "rtc.RemoteTrackPublication",
    "rtc.DataPacket",
    # Riva dependencies
    "riva",
    "riva.client",
    "riva.client.Auth",
    "riva.client.ASRService",
    "riva.client.StreamingRecognitionConfig",
    "riva.client.RecognitionConfig",
    "riva.client.AudioEncoding",
    "riva.client.proto.riva_tts_pb2",
    "riva.client.SpeechSynthesisService",
    # Local CoreML Smart Turn dependencies
    "coremltools",
    "coremltools.models",
    "coremltools.models.MLModel",
    "torch",
    "torch.nn",
    "torch.nn.functional",
    "transformers",
    "transformers.AutoFeatureExtractor",
    # Also add specific classes that are imported
    "AutoFeatureExtractor",
    # Sentry dependencies
    "sentry_sdk",
    # AWS Nova Sonic dependencies
    "aws_sdk_bedrock_runtime",
    "aws_sdk_bedrock_runtime.client",
    "aws_sdk_bedrock_runtime.config",
    "aws_sdk_bedrock_runtime.models",
    "smithy_aws_core",
    "smithy_aws_core.credentials_resolvers",
    "smithy_aws_core.credentials_resolvers.static",
    "smithy_aws_core.identity",
    "smithy_core",
    "smithy_core.aio",
    "smithy_core.aio.eventstream",
    # MCP dependencies (you may already have these)
    "mcp",
    "mcp.client",
    "mcp.client.session_group",
    "mcp.client.sse",
    "mcp.client.stdio",
    "mcp.ClientSession",
    "mcp.StdioServerParameters",
]

# HTML output settings
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
autodoc_typehints = "description"
html_show_sphinx = False


def verify_modules():
    """Verify that required modules are available."""
    required_modules = {
        "services": [
            "assemblyai",
            "aws",
            "cartesia",
            "deepgram",
            "google",
            "lmnt",
            "riva",
            "simli",
        ],
        "serializers": ["livekit"],
        "vad": ["silero", "vad_analyzer"],
        "transports": {
            "services": ["daily", "livekit"],
            "local": ["audio", "tk"],
            "network": ["fastapi_websocket", "websocket_server"],
        },
    }

    # Skip importing modules that are in autodoc_mock_imports
    skipped_modules = set(autodoc_mock_imports)

    missing = []
    for category, modules in required_modules.items():
        if isinstance(modules, dict):
            # Handle nested structure
            for subcategory, submodules in modules.items():
                for module in submodules:
                    # Check if module is in autodoc_mock_imports
                    if (
                        f"pipecat.{category}.{subcategory}.{module}" in skipped_modules
                        or module in skipped_modules
                    ):
                        logger.info(
                            f"Skipping import of mocked module: pipecat.{category}.{subcategory}.{module}"
                        )
                        continue

                    try:
                        __import__(f"pipecat.{category}.{subcategory}.{module}")
                        logger.info(
                            f"Successfully imported pipecat.{category}.{subcategory}.{module}"
                        )
                    except (ImportError, TypeError, NameError) as e:
                        missing.append(f"pipecat.{category}.{subcategory}.{module}")
                        logger.warning(
                            f"Optional module not available: pipecat.{category}.{subcategory}.{module} - {str(e)}"
                        )
        else:
            # Handle flat structure
            for module in modules:
                # Check if module is in autodoc_mock_imports
                if f"pipecat.{category}.{module}" in skipped_modules or module in skipped_modules:
                    logger.info(f"Skipping import of mocked module: pipecat.{category}.{module}")
                    continue

                try:
                    __import__(f"pipecat.{category}.{module}")
                    logger.info(f"Successfully imported pipecat.{category}.{module}")
                except (ImportError, TypeError, NameError) as e:
                    missing.append(f"pipecat.{category}.{module}")
                    logger.warning(
                        f"Optional module not available: pipecat.{category}.{module} - {str(e)}"
                    )

    if missing:
        logger.warning(f"Some optional modules are not available: {missing}")


def clean_title(title: str) -> str:
    """Automatically clean module titles."""
    # Remove everything after space (like 'module', 'processor', etc.)
    title = title.split(" ")[0]

    # Get the last part of the dot-separated path
    parts = title.split(".")
    title = parts[-1]

    # Special cases for service names and common acronyms
    special_cases = {
        "ai": "AI",
        "aws": "AWS",
        "api": "API",
        "vad": "VAD",
        "assemblyai": "AssemblyAI",
        "deepgram": "Deepgram",
        "elevenlabs": "ElevenLabs",
        "openai": "OpenAI",
        "openpipe": "OpenPipe",
        "playht": "PlayHT",
        "xtts": "XTTS",
        "lmnt": "LMNT",
        "stt": "STT",
        "tts": "TTS",
        "llm": "LLM",
    }

    # Check if the entire title is a special case
    if title.lower() in special_cases:
        return special_cases[title.lower()]

    # Otherwise, capitalize each word
    words = title.split("_")
    cleaned_words = []
    for word in words:
        if word.lower() in special_cases:
            cleaned_words.append(special_cases[word.lower()])
        else:
            cleaned_words.append(word.capitalize())

    return " ".join(cleaned_words)


def setup(app):
    """Generate API documentation during Sphinx build."""
    from sphinx.ext.apidoc import main

    docs_dir = Path(__file__).parent
    project_root = docs_dir.parent.parent
    output_dir = str(docs_dir / "api")
    source_dir = str(project_root / "src" / "pipecat")

    # Clean existing files
    if Path(output_dir).exists():
        import shutil

        shutil.rmtree(output_dir)
        logger.info(f"Cleaned existing documentation in {output_dir}")

    logger.info(f"Generating API documentation...")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Source directory: {source_dir}")

    excludes = [
        str(project_root / "src/pipecat/pipeline/to_be_updated"),
        str(project_root / "src/pipecat/processors/gstreamer"),
        str(project_root / "src/pipecat/services/to_be_updated"),
        str(project_root / "src/pipecat/vad"),  # deprecated
        "**/test_*.py",
        "**/tests/*.py",
    ]

    try:
        main(
            [
                "-f",  # Force overwriting
                "-e",  # Don't generate empty files
                "-M",  # Put module documentation before submodule documentation
                "--no-toc",  # Don't create a table of contents file
                "--separate",  # Put documentation for each module in its own page
                "--module-first",  # Module documentation before submodule documentation
                "--implicit-namespaces",  # Added: Handle implicit namespace packages
                "-o",
                output_dir,
                source_dir,
            ]
            + excludes
        )

        logger.info("API documentation generated successfully!")

        # Process generated RST files to update titles
        for rst_file in Path(output_dir).glob("**/*.rst"):  # Changed to recursive glob
            content = rst_file.read_text()
            lines = content.split("\n")

            # Find and clean up the title
            if lines and "=" in lines[1]:  # Title is typically the first line
                old_title = lines[0]
                new_title = clean_title(old_title)
                content = content.replace(old_title, new_title)
                rst_file.write_text(content)
                logger.info(f"Updated title: {old_title} -> {new_title}")

    except Exception as e:
        logger.error(f"Error generating API documentation: {e}", exc_info=True)


# Run module verification
verify_modules()
