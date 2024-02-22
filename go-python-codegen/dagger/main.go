package main

import (
	"bytes"
	"context"
	"embed"
	"strings"
	"text/template"
)

//go:embed templates
var tmpls embed.FS

type GoPythonCodegen struct {}

func (m *GoPythonCodegen) ObjectNames(ctx context.Context) (string, error) {
    funcs := template.FuncMap{
        "Get": func(f func (context.Context) (any, error)) any {
            v, err := f(ctx)
            if err != nil {
                panic(err)
            }
            return v
        },
        "ctx": func () context.Context {
            return ctx
        },
        "ToSnake": func (s string) string {
            return strings.ReplaceAll(strings.ToLower(s), " ", "_")
        },
    }

	tmpl, err := template.New("python").Funcs(funcs).ParseFS(tmpls, "templates/*.tmpl")
	if err != nil {
        return "", err
	}

    /*
    json_str, err := dag.Codegen().Introspect().AsJSON(ctx)
    if err != nil {
        return "", err
    }

    var data any

    if err := json.Unmarshal([]byte(json_str), &data); err != nil {
        return "", err
    }
    */

    buf := new(bytes.Buffer)
	err = tmpl.ExecuteTemplate(buf, "python.tmpl", dag.Codegen().Introspect())
	if err != nil {
        return "", err
	}

    return buf.String(), nil
}
