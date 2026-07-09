# Spec: vision-serving-fastapi

## Number

#7

## Claim

Este projeto prova que: servir modelo CV.

## Stack

python, fastapi, onnxruntime, prometheus, k6, docker

## User-visible output

- Docker command: pending
- README opens with: # #7 vision-serving-fastapi
- Benchmark table: throughput_rps, p95_latency_ms

## Scope

In:

- Implementar o menor produto funcional que prove o claim.
- Rodar por Docker.
- Gerar benchmark JSON reproduzivel.

Out:

- Publicar repo antes do primeiro resultado numerico.
- Depender de segredo pago para o caminho default.

## Architecture

`	xt
client -> app -> domain -> adapters -> benchmark output
`

## Benchmark

Primary metric:

- name: throughput_rps, p95_latency_ms
- target: first reproducible baseline
- command: pending
- result file: enchmarks/results/*.json

## Dataset or fixture

- source: pending
- size: pending
- license: pending
- deterministic seed: 42

## Definition of done

- [ ] Docker command works from clean clone.
- [ ] README starts with project number and benchmark result.
- [ ] Benchmark command writes JSON result.
- [ ] Tests cover core behavior.
- [ ] REFERENCES.md explains reuse.
- [ ] No secret or paid credential required for default demo.