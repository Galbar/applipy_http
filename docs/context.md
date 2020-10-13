# Context

Context is a `collections.abc.Mapping` that can be used to store information
while processing a HTTP request.

It is specially useful when combined with
[`EndpointWrapper`s](endpoint_wrapper.md) to do pre-processing in them and then
use the result in the `Endpoint` methods.
