import time


def wait_for_va_completion(service, wanted, done, final_status, timeout,
                           interval=2.0, grace_polls=3) -> bool:
    """Wait for VA pipelines to finish.

    Completion is signalled by any of:
      1. the on_all_pipelines_done callback (``done`` set),
      2. the service already recording a terminal status (eos/failed) for every
         wanted pipeline in ``service.pipeline_final_status``,
      3. every wanted pipeline process having exited (``is_pipeline_running``
         returns False) for ``grace_polls`` consecutive polls -- a fallback that
         catches completion even when the callback and status recording fail.

    On completion, ``final_status`` is refreshed from the service so callers can
    judge success/failure from the recorded per-pipeline statuses.

    Returns True on completion, False if ``timeout`` elapsed first.
    """
    deadline = time.monotonic() + timeout
    down_count = 0
    while time.monotonic() < deadline:
        if done.is_set():
            final_status.update(service.pipeline_final_status)
            return True
        statuses = service.pipeline_final_status
        if statuses and all(statuses.get(n) in ("eos", "failed") for n in wanted):
            final_status.update(statuses)
            return True
        all_down = all(not service.is_pipeline_running(n) for n in wanted)
        if all_down:
            down_count += 1
            if down_count >= grace_polls:
                final_status.update(service.pipeline_final_status)
                return True
        else:
            down_count = 0
        time.sleep(interval)
    return False
