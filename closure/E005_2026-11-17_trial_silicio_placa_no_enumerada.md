# E005 — 2026-11-17 — Trial con silicio (trial_v3): placa reconectada antes de que el depurador estuviera listo

## Hecho
Primer par del trial con silicio (pre-registrado en el sello 26), ambas corridas FAIL solo en la fase 12:
- OFFLINE `AXIOM_TRIAL_20261117T182557Z`: fases 0-11 PASS. En la fase 12, la KAT, S3, S4-A (18/18), S4-B y S5 dieron PASS
  (evidencia `silicio/evidence/s345_20261117T190709Z`). Fallo la lectura final tras el 2.o corte: `placa_lee.txt` =
  "Error: No connected probes were found."
- ONLINE `AXIOM_TRIAL_20261117T191154Z`: fase 0 FAIL (sin contraparte OFFLINE ALL PASS, correcto) y fase 12 FAIL: tras el
  1.er corte, `placa_s3s4a.txt` = "No connected probes were found"; en consecuencia S4-B encontro el testigo sin ceremonia
  (B0 FAIL, consecuencia esperada). S5 y la lectura final PASS (LEE LIMPIO: PGD=1, MC=0, LPGPR=0).

## Diagnostico
Error del operador, confirmado por el propio operador: se pulso Enter inmediatamente despues de reconectar el USB, antes
de que el DAPLink de la placa enumerara (unos segundos). probe-rs no encontro el depurador y la fase no corrio.
No es un fallo del kernel, del firmware ni de los teoremas: ninguna verificacion dio un resultado contrario; cada
verificacion que si se ejecuto dio PASS. La placa quedo en estado de fabrica (lectura de la corrida ONLINE).

## Correccion
Sin cambios de codigo (nada sellado se toca; el pre-registro del sello 26 sigue vigente). Procedimiento del operador:
tras reconectar, esperar a que la luz de la placa encienda y contar 10 s mas antes de pulsar Enter.
Se repite el par OFFLINE + ONLINE. Las dos corridas fallidas se conservan en `trial_v3/runs/` y se sellan como registro
junto con el par que pase.
