import json
import pdb
import requests
import sys

from typing import TypedDict, Union

from stoobly_agent.app.cli.helpers.handle_replay_service import JSON_FORMAT, format_request, print_with_decoding
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.types.output import TestOutput
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import bcolors
from stoobly_agent.lib.utils.decode import decode

from .test_replay_context import TestReplayContext

class HandleOptions(TypedDict):
  format: str

class SessionContext(TypedDict):
  aggregate_failures: bool 
  passed: int
  output: TestOutput
  project_id: int
  skipped: int
  test_facade: TestFacade
  total: int

class ExitOnFailureOptions(TypedDict):
  complete: bool
  format: Union[str, None] 

def handle_test_session_complete(session_context: SessionContext, **options: HandleOptions):
  format = options.get('format')
  format_handler = __default_session_complete_formatter

  if format == JSON_FORMAT:
    format_handler = __json_session_complete_formatter

  format_handler(session_context)

def handle_test_complete(
  context: ReplayContext, session_context: SessionContext, **options: HandleOptions 
):
  format = options.get('format')
  format_handler = __default_test_complete_formatter

  if format == JSON_FORMAT:
    format_handler = __json_test_complete_formatter

  context = TestReplayContext(context)
  if not context.has_test_results:
    context.project_id = session_context['project_id']

  test = context.test_show_response(session_context['test_facade'])

  if test['skipped']:
    session_context['skipped'] += 1

  passed = bool(test.get('passed')) if isinstance(test, dict) else False
  session_context['passed'] += (1 if passed else 0)
  session_context['total'] += 1

  format_handler(context, session_context, test)

def exit_on_failure(session_context: SessionContext, **options: ExitOnFailureOptions):
  complete = options.get('complete') 
  if complete == None:
    complete = True

  if session_context['passed'] + session_context['skipped'] != session_context['total']:
    if not complete:
      handle_test_session_complete(session_context, format=options.get('format'))

    sys.exit(1)

def __json_test_complete_formatter(context: ReplayContext, session_context: SessionContext, res: TestShowResponse):
  if 'output' not in session_context:
    session_context['output'] = {}

  output = session_context['output']
  if not res:
    output['error'] = 'Test failed to run'
  elif isinstance(res, str):
    output['error'] = res
  else:
    if 'tests' not in output:
      output['tests'] = []

    seconds = context.end_time - context.start_time
    latency = round(seconds * 1000)
    test = {
      'log': res['log'] if 'log' in res else '',
      'passed': res['passed'],
      'response': { **__build_json_response(context.response), 'latency': latency} 
    }

    if not res['passed']:
      project_id = session_context['project_id']
      test_facade = session_context['test_facade']
      expected_response = __get_test_expected_response_with_context(context, project_id, test_facade)

      if expected_response:
        test['expected_response'] = { **__build_json_response(expected_response), 'latency': res['expected_latency']}

    output['tests'].append(test)

def __default_test_complete_formatter(context: ReplayContext, session_context: SessionContext, res: TestShowResponse):
  if not res:
    print_with_decoding(format_request(context))
    print("\nTest failed to run")
  elif isinstance(res, str):
    print(res, file=sys.stderr)
  else:
    print_with_decoding(format_request(context))

    if not res['passed']:
      if res['skipped']:
        passed_message = f"{bcolors.WARNING}skipped{bcolors.ENDC}"
      else:
        passed_message = f"{bcolors.FAIL}failed{bcolors.ENDC}"
    else:
      passed_message = f"{bcolors.OKGREEN}passed{bcolors.ENDC}"

    print(f"\nTest {passed_message} using {bcolors.BOLD}{res['strategy']}{bcolors.ENDC} strategy")
    
    if res['log']:
      print(res['log'])

    if not res['passed'] and not res['skipped']:
      project_id = session_context['project_id']
      test_facade = session_context['test_facade']
      expected_response = __get_test_expected_response_with_context(context, project_id, test_facade)

      if expected_response:
        if isinstance(expected_response, requests.Response):
          print(f"\n{bcolors.BOLD}Expected Response{bcolors.ENDC}")
          print(__decode_response(expected_response))
          print(f"Completed {expected_response.status_code} in {res['expected_latency']}ms")
        else:
          print("API Error: Invalid response")

def __default_session_complete_formatter(session_context: SessionContext):
  if 'output' in session_context:
    print(session_context['output'])

  total = session_context['total']

  if total > 1:
    passed = session_context['passed']
    skipped = session_context['skipped']

    passed_message = f"{passed} / {total} {bcolors.OKGREEN}passed{bcolors.ENDC}"

    skipped_message = ''
    if skipped:
      skipped_message = f" {skipped} {bcolors.WARNING}skipped{bcolors.ENDC}"

    if passed == total:
      print(f"\n{passed_message}{skipped_message}")
    else:
      failed_message = f"{total - passed - skipped} {bcolors.FAIL}failed{bcolors.ENDC}"
      print(f"\n{passed_message} {failed_message}{skipped_message}")

def __json_session_complete_formatter(session_context: SessionContext):
  if 'output' not in session_context:
    return

  session_context['output']['passed'] = session_context['passed']
  session_context['output']['skipped'] = session_context['skipped']
  session_context['output']['total'] = session_context['total']

  print(json.dumps(session_context['output']))

def __get_test_expected_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade) -> Union[requests.Response, str]:
  try:
    res = test_facade.expected_response_with_context(context, project_id)
    return res
  except AssertionError as e:
    return f"API Error: {e}"

def __build_json_response(response: requests.Response):
  return {
    'content': __decode_response(response),
    'status_code': response.status_code,
  }

def __decode_response(response: requests.Response):
  if isinstance(response, requests.Response):
    content = response.content
    return decode(content)
  else:
    return "API Error: Internal Error"