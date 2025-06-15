# Notes

Debug this error next:

- start both services
- make a request to `/sets/exercise/{exercise_id}` e.g. 1 -> Bench Press
- you should see the error in the terminal

```bash
uvicorn backend.main:app --reload --host
```

```plaintext
Traceback (most recent call last):
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 399, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 70, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/applications.py", line 123, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
    raise exc
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 65, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/routing.py", line 756, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/routing.py", line 776, in app
    await route.handle(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/routing.py", line 297, in handle
    await self.app(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/routing.py", line 77, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 64, in wrapped_app
    raise exc
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/routing.py", line 72, in app
    response = await func(request)
               ^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 278, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/fastapi/routing.py", line 193, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/starlette/concurrency.py", line 42, in run_in_threadpool
    return await anyio.to_thread.run_sync(func, *args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/anyio/to_thread.py", line 56, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 2177, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/anyio/_backends/_asyncio.py", line 859, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/backend/routers/sets.py", line 133, in get_sets_by_exercise
    packed_results = msgpack.packb(results_dict, use_bin_type=True)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/christian/Projects/workoutHub/.venv/lib/python3.12/site-packages/msgpack/__init__.py", line 36, in packb
    return Packer(**kwargs).pack(o)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "msgpack/_packer.pyx", line 279, in msgpack._cmsgpack.Packer.pack
  File "msgpack/_packer.pyx", line 276, in msgpack._cmsgpack.Packer.pack
  File "msgpack/_packer.pyx", line 270, in msgpack._cmsgpack.Packer._pack
  File "msgpack/_packer.pyx", line 232, in msgpack._cmsgpack.Packer._pack_inner
  File "msgpack/_packer.pyx", line 270, in msgpack._cmsgpack.Packer._pack
  File "msgpack/_packer.pyx", line 213, in msgpack._cmsgpack.Packer._pack_inner
  File "msgpack/_packer.pyx", line 270, in msgpack._cmsgpack.Packer._pack
  File "msgpack/_packer.pyx", line 257, in msgpack._cmsgpack.Packer._pack_inner
TypeError: can not serialize 'datetime.datetime' object
```