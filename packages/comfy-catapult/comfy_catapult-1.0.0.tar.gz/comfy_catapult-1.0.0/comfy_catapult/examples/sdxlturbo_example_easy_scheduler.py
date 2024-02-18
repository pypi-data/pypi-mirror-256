import argparse
import asyncio
import sys
import uuid
from urllib.parse import ParseResult, urljoin, urlparse

from anyio import Path
from comfy_scheduler.comfy_client import _YamlDump
from comfy_scheduler.comfy_scheduler_base import ComfySchedulerGeneric
from comfy_scheduler.comfy_schema import APIWorkflow
from comfy_scheduler.remote_file_api import ComfyBaseURLConfig, RemoteBaseURL


async def amain():

  def URL_HELP(to: str, example_url: str, default_subdir: str | None):
    lines = [
        f"URL to ComfyUI {to} directory, e.g. {repr(example_url)}.",
        "Note, that the URL must end with a trailing slash.",
    ]
    if default_subdir is not None:
      lines += [f"Defaults to comfy_base_url + '{default_subdir}'."]
    return ' '.join(lines)

  parser = argparse.ArgumentParser()
  parser.add_argument('--comfy_api_url',
                      type=urlparse,
                      default='http://127.0.0.1:8188')
  parser.add_argument('--api_workflow_json_path', type=Path, required=True)
  parser.add_argument(
      '--comfy_base_url',
      type=urlparse,
      required=True,
      help=URL_HELP("install",
                    "file:///mnt/d/stability-matrix-data/Packages/ComfyUI/",
                    None))

  parser.add_argument(
      '--comfy_input_url',
      type=urlparse,
      default=None,
      help=URL_HELP(
          "input",
          "file:///mnt/d/stability-matrix-data/Packages/ComfyUI/input/",
          "input/"))
  parser.add_argument(
      '--comfy_output_url',
      type=urlparse,
      default=None,
      help=URL_HELP(
          "output",
          "file:///mnt/d/stability-matrix-data/Packages/ComfyUI/output/",
          "output/"))
  parser.add_argument('--tmp_path', type=Path, required=True)
  parser.add_argument('--output_path', type=Path, required=True)
  args = parser.parse_args()

  # Unpack some arguments for convenience.

  ##############################################################################
  comfy_api_url_pr: ParseResult = args.comfy_api_url
  comfy_api_url = comfy_api_url_pr.geturl()
  ##############################################################################
  api_workflow_json_path: Path = args.api_workflow_json_path
  ##############################################################################
  comfy_base_url_pr: ParseResult = args.comfy_base_url

  comfy_input_url_pr: ParseResult | None = args.comfy_input_url
  comfy_output_url_pr: ParseResult | None = args.comfy_input_url
  if comfy_input_url_pr is None:
    comfy_input_url_pr = urlparse(urljoin(comfy_base_url_pr.geturl(), 'input/'))
  if comfy_output_url_pr is None:
    comfy_output_url_pr = urlparse(
        urljoin(comfy_base_url_pr.geturl(), 'output/'))

  comfy_base_url = comfy_base_url_pr.geturl()
  comfy_input_url = comfy_input_url_pr.geturl()
  comfy_output_url = comfy_output_url_pr.geturl()
  ##############################################################################
  tmp_path: Path = args.tmp_path
  ##############################################################################
  output_path: Path = args.output_path
  ##############################################################################

  # comfy_input_bases = ComfyBaseURLConfig(
  #     user_base=RemoteBaseURL(
  #         base_url=
  #         'file:///mnt/d/stability-matrix-data/Packages/ComfyUI/input/'),
  #     io_base=RemoteBaseURL(
  #         base_url=
  #         'file:///mnt/d/stability-matrix-data/Packages/ComfyUI/input/'),
  #     comfy_base=RemoteBaseURL(
  #         base_url='file:///mnt/d/stability-matrix-data/Packages/ComfyUI/'))
  # comfy_output_bases = ComfyBaseURLConfig(
  #     user_base=RemoteBaseURL(
  #         base_url=
  #         'file:///mnt/d/stability-matrix-data/Packages/ComfyUI/output/'),
  #     io_base=RemoteBaseURL(
  #         base_url=
  #         'file:///mnt/d/stability-matrix-data/Packages/ComfyUI/output/'),
  #     comfy_base=RemoteBaseURL(
  #         base_url='file:///mnt/d/stability-matrix-data/Packages/ComfyUI/'))

  # These are used to insure that files are not written/read outside of the
  # comfy_input_url and comfy_output_url directories.
  comfy_input_bases = ComfyBaseURLConfig(
      user_base=RemoteBaseURL(url=comfy_input_url),
      io_base=RemoteBaseURL(url=comfy_input_url),
      comfy_base=RemoteBaseURL(url=comfy_base_url))

  comfy_output_bases = ComfyBaseURLConfig(
      user_base=RemoteBaseURL(url=comfyui_output_url),
      io_base=RemoteBaseURL(url=comfyui_output_url),
      comfy_base=RemoteBaseURL(url=comfyui_base_url))
  comfy_config = RemoteComfyConfig(
      comfy_api_url=comfy_api_url,
      base_url=comfy_base_url,
      input_url=comfy_input_url,
      output_url=comfy_output_url,
  )

  api_workflow_json_str: str = await api_workflow_json_path.read_text()
  api_workflow: APIWorkflow = APIWorkflow.model_validate_json(
      api_workflow_json_str)

  async with ComfySchedulerGeneric(callback=SimpleComfyCallback(),
                                   params=SimpleComfyScheduler.SchedulerParams(
                                       comfyui_api_url=comfyui_api_url,
                                       comfy_input_bases=comfy_input_bases,
                                       comfy_output_bases=comfy_output_bases,
                                       workflow=api_workflow,
                                       tmp_path=tmp_path)) as scheduler:
    job_id = str(uuid.uuid4())

    status, future = await scheduler.Schedule(
        job_id=job_id,
        inputs=SimpleComfyInput(checkpoint_name=checkpoint_name,
                                output_path=output_path))
    print('status:', file=sys.stderr)
    print(_YamlDump({'status': status._asdict()}), file=sys.stderr)

    result = await future


asyncio.run(amain(), debug=True)
