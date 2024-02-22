// Codegen for the Dagger API
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"sort"
	"strings"

	"github.com/Khan/genqlient/graphql"
)

type Codegen struct { }

// Get the GraphQL query used to get type information
func (*Codegen) IntrospectionQuery() string {
	return query
}

// Introspect the API to get the schema
//
// The schema information is used to generate the client code.
func (*Codegen) Introspect(
	ctx context.Context,
	// A file with the result of the introspection query, in JSON format
    //
    // In runtime modules, the codegen function receives the contents of
    // this file, which already filters out the runtime module itself from
    // the results.
	// +optional
	fromJSON *File,
) (*Schema, error) {
	var resp response

	if fromJSON != nil {
		jsonIntrospection, err := fromJSON.Contents(ctx)
		if err != nil {
			return nil, fmt.Errorf("read introspection file: %w", err)
		}
		if err := json.Unmarshal([]byte(jsonIntrospection), &resp); err != nil {
			return nil, fmt.Errorf("unmarshal introspection json: %w", err)
		}
	} else {
		err := dag.c.MakeRequest(ctx, &graphql.Request{
			Query:  query,
			OpName: "IntrospectionQuery",
		}, &graphql.Response{
			Data: &resp,
		})
		if err != nil {
			return nil, fmt.Errorf("introspection query: %w", err)
		}
	}

	return resp.Schema.update(), nil
}

// Result of the introspection, in JSON format
func (s *Schema) AsJSON() (string, error) {
	b, err := json.MarshalIndent(s, "", "  ")
    if err != nil {
        return "", err
    }
	return string(b), nil
}

func (s *Schema) update() *Schema {
	return s.sorted().splitNames()
}

func (s *Schema) sorted() *Schema {
	types := []*Type{}

	for _, t := range s.Types {
		if strings.HasPrefix(t.Name, "__") {
			continue
		}
        // Skip current module
        if strings.HasPrefix(t.Name, "Codegen") {
            continue
        }
        // Rename Query to Client
        if t.Name == "Query" {
            t.Name = rootObjectName
        }
		types = append(types, t)
	}

	// Sort types
	sort.Slice(types, func(i, j int) bool {
		return types[i].Name < types[j].Name
	})

	// Sort within the type
	for _, t := range types {
		sort.Slice(t.Fields, func(i, j int) bool {
			return t.Fields[i].Name < t.Fields[j].Name
		})
		sort.Slice(t.InputFields, func(i, j int) bool {
			return t.InputFields[i].Name < t.InputFields[j].Name
		})
	}

	s.Types = types
	return s
}

func (s *Schema) splitNames() *Schema {
	for _, t := range s.Types {
		for _, f := range t.Fields {
			f.NameWords = splitName(f.Name)
			for _, a := range f.Args {
				a.NameWords = splitName(a.Name)
			}
		}
	}
	return s
}

