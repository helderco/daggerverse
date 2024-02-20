package main

import "context"

// Experimental alternative to the introspection query, using the TypeDef API
//
// TypeDefs require more requests than the introspection query, and some
// types haven't been implemented yet, but they may provide more context
// like the module name that implements an object type, for example.
func (*Codegen) Experimental() *Experimental {
   return &Experimental{}
}

// Experimental alternative to the introspection query, using the TypeDef API
type Experimental struct { }

// Get the names of all object types in the API
//
// Allows querying the API directly while filtering out the current module.
// It does take more requests, compared to the introspection query which
// takes a single request, or the introspection file which takes no requests.
// However when this module is consumed, there's an exec to /runtime on
// every function call.
func (e *Experimental) ObjectNames(ctx context.Context) ([]string, error) {
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

// Get the names of all input object types in the API
//
// Only object types have an associated module name because input types
// (and others) are only used in the core API. Modules don't expose either
// custom scalars, enums, or interfaces, for example.
func (e *Experimental) InputNames(ctx context.Context) ([]string, error) {
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

