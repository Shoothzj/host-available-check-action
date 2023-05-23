# host-available-check-action

This is a GitHub Action that verifies if a host is available and responsive.

## Inputs

- `check_type`: The type of check to perform. Possible values are 'HTTP' and 'TCP'.
- `check_timeout`: The maximum amount of time (in seconds) to wait for the check to pass.
- `check_http_port`: The HTTP port to check. Default is 80. This is used when `check_type` is 'HTTP'.
- `check_http_path`: The HTTP path to check. This is used when `check_type` is 'HTTP'.
- `check_tcp_port`: The TCP port to check. Default is 80. This is used when `check_type` is 'TCP'.

## Usage

To use this action in your workflow, you need to set it up as a step:

```yaml
steps:
- uses: actions/checkout@v3
- uses: shoothzj/host-available-check-action@v1
  with:
    check_type: 'HTTP'
    check_timeout: 60
    check_http_port: 8080
    check_http_path: '/api/health'
```

In the above example, we're checking if the HTTP server is responding on port 8080 and path /api/health. The check will timeout after 60 seconds if the server is unresponsive.
