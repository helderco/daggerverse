package main

import "context"

// Experimental alternative to the introspection query
//
// Allows querying the API directly while filtering out the current module.
// It does take more requests, compared to the introspection query which
// takes a single request, or the introspection file which takes no requests.
// However when this module is consumed, there's an exec to /runtime on
// every function call.
func (c *Codegen) ExperimentalObjectNames(ctx context.Context) ([]string, error) {
	names := []string{}

	modName, err := dag.CurrentModule().Name(ctx)
	if err != nil {
		return nil, err
	}

	types, err := dag.CurrentTypeDefs(ctx)
	if err != nil {
		return nil, err
	}

	for _, t := range types {
		o := t.AsObject()

		s, err := o.SourceModuleName(ctx)
		if err != nil {
			return nil, err
		}

		if s == modName {
			continue
		}

		name, err := o.Name(ctx)
		if err != nil {
			return nil, err
		}

		if name != "" {
			names = append(names, name)
		}
	}

	return names, nil
}

// Experimental alternative to the introspection query
//
// Only object types have an associated module name because input types
// (and others) are only used in the core API. Modules don't expose either
// custom scalars, enums, or interfaces, for example.
func (c *Codegen) ExperimentalInputNames(ctx context.Context) ([]string, error) {
	names := []string{}

	types, err := dag.CurrentTypeDefs(ctx)
	if err != nil {
		return nil, err
	}

	for _, t := range types {
		name, err := t.AsInput().Name(ctx)
		if err != nil {
			return nil, err
		}

		if name != "" {
			names = append(names, name)
		}
	}

	return names, nil
}

