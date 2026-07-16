# Repository Boundaries

services/api owns HTTP routes, request validation, order application services, and API tests. apps/web owns the operations interface, React server and client boundaries, styling, and browser-facing tests. automation owns repository metadata used by continuous integration and has no application runtime.

The API and web application are independently buildable. Changes that cross their public contract require both focused suites. Automation changes use configuration validation and do not activate an application language skill solely because they describe Python or Node commands as data.
