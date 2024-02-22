# Dagger codegen module

This module is an experiment in testing the viability of simplifying codegen
implementations in Dagger SDKs using a module.

This is done by centralizing the [GraphQL introspection][gqli], and
pre-processing the data needed for templates as much as possible, as described
in the [Improve codegen reusibility][5226] issue.

This lowers the barrier of entry for new SDKs, but also makes it a lot easier
to maintain existing SDKs and keep them consistent with each other.

[gqli]: https://graphql.org/learn/introspection/
[5226]: https://github.com/dagger/dagger/issues/5226

Here's just a few examples of repeated logic that SDKs make today, without this
abstraction layer:
- When to execute query vs chain?
- When to convert from ID to object?
- Which field to request for the corresponding object from ID?
- Is type id-able?
- Is type self-chainable (add `With` method)?
- Format names consistently
- Custom errors/exception types
- Sort types, fields and arguments to be deterministic
- Rename "Query" type to "Client"
- Rename deprecated field name in deprecation reason


## Usage

The main use case is to use this in the Codegen function of a runtime module
as a dependency, but the introspection is so easy to access now that it may
unlock other interesting use cases as well. It could be used, for example,
to create a GUI to interact with the API.


### Examples

- `dagger call introspection-query`
- `dagger call introspect as-json`
- `dagger call introspect scalars name`
- `dagger call introspect enums name`
- `dagger call introspect objects name`
- `dagger call introspect get-type --name=Container fields name-words`
- `dagger call introspect get-type --name=Container get-field --name=withExec optional-args name`

## Performance

Unfortunately the performance isn't good when used from an SDK's client. Even
though the introspection makes a single request to the API to get all type
information, and is quick to pre-process the data, consumers still need to
access each leaf individually, making many requests to access all the data.

Resolving the following issues could help with this:
- [Codegen: Selecting sibling fields](https://github.com/dagger/dagger/issues/3577)
- [Codegen: Return simple objects](https://github.com/dagger/dagger/issues/4920)

But there's more we can explore:
- Get all logic in fields (no functions), to avoid an `exec /runtime` trip.
- Use interfaces and invert control, i.e., make the codegen module "visit" user functions.
- Return the whole data structure in OpenAPI.


## What's next?

- Configuration for specifying a language's naming convention for field, argument
  and type names.
- Move introspection unmarshalling to a sub-package, and process data into
  a new data structure, fine tuned for Dagger codegen.
- Include custom Dagger errors.
- Include module information when doing codegen for a module.
- Explore solution with interfaces.
- Reimplement [Python codegen](../python-codegen) and make it a reference for
  other languages.
