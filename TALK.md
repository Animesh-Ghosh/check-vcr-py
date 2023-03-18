# Speeding up HTTP tests using VCR.py

## What is VCR.py

- library for recording HTTP requests and replaying them back
- primary use-case is in creating "cassettes",
- port of Ruby's VCR gem

## Why use VCR.py

- speed up your test suite
- get deterministic tests, for the same params expect the same responses
- save costs if APIs are rate-limited

## Basic Usage

*Demo*

## Custom Serializers

*Demo*

## Matchers

- What is a matcher in VCR.py?
- defaults for match_on = ['method', 'scheme', 'host', 'port', 'path', 'query']

*Demo*

## Further readings and resources

- [Docs](https://vcrpy.readthedocs.io/en/latest/index.html)
- [Advanced Usage, such as writing custom serializers and sensitive data filtering in cassettes](https://vcrpy.readthedocs.io/en/latest/advanced.html)
- [OG VCR repository](https://github.com/vcr/vcr)