1) В папке dify-docs лежат скачанные с GitHub dify.ai исходные документы.

2) В папке in_notebooks лежат исследования, промежуточные результаты и метрики исследований.

3) В папке in_notebooks/chunks содержится порезанная на чанки разными стратегиями документация.

4) В папке in_notebooks/eval_text_metrics_BLEU_ROUGEL_BERTScore содержатся результаты оценки генерации по вопросам из golden сета на основании чанков, созданных по разным стратегиям и найденных разными ретриверами, созданными на основании модели e5-large-v2.

5) В папке in_notebooks/eval_text_metrics_BLEU_ROUGEL_BERTScore_bge_large содержатся результаты оценки генерации по вопросам из golden сета на основании чанков, созданных по разным стратегиям и найденных разными ретриверами, созданными на основании модели bge large en v1.5.

6) В in_notebooks/golden_sets содержатся указания названий чанков, созданных разными стратегиями чанкования, в которых содержатся ответы на вопросы из golden сета.

7) В in_notebooks/metrics содержатся метрики по работе ретриверов BM25, dense и их гибрида по каждой из стратегий чанкования. Ретривер на основании модели e5-large-v2.

8) В in_notebooks/metrics/metrics_dense_vs_cross_enc/metrics_cross_bge_reranker хранятся метрики по чанкам, найденным с применением реранкера, но найденных изначально на основании e5-large-v2.

9) В in_notebooks/metrics_bge_large_en_v_poltora содержатся метрики по работе ретриверов BM25, dense и их гибрида по каждой из стратегий чанкования. Ретривер на основании модели bge large en v1.5.

10) В in_notebooks/metrics_bge_large_en_v_poltora/metrics_dense_vs_cross_enc/metrics_cross_bge_reranker хранятся метрики по чанкам, найденным с применением реранкера, но найденных изначально на основании bge large en v1.5.

11) В in_notebooks/rag_outputs хранятся сгенерированные e5-large-v2 ответы по вопросам golden сета на основании разных конфигураций.

12) В in_notebooks/rag_outputs_bge_large хранятся сгенерированные bge large en v1.5 ответы по вопросам golden сета на основании разных конфигураций.

13) В in_notebooks/golden_master.json содержатся вопросы, эталонные ответы на них, документы и части документов, в которых содержится ответ на вопросы.

14) В in_notebooks/parsed_structure.jsonl содержится структура документации из dify-docs.

15) В папке project содержится проект — проект запускается из директории project через docker compose build и docker compose up.

16) В in_notebooks/results содержатся результаты найденных чанков по каждой из конфигураций стратегий по каждому из ретриверов (results_bm25, results_dense, results_hybrid) на базе модели e5-large-v2.

17) В in_notebooks/results/results_reranker_bge — пересобранные реранкером чанки, найденные изначально e5-large-v2.

18) В in_notebooks/results_bge_large_en_v15 содержатся результаты найденных чанков по каждой из конфигураций стратегий по каждому из ретриверов (results_bm25_bge_large, results_dense_bge_large, results_hybrid_bge_large) на базе модели bge large en v1.5.

19) В in_notebooks/results_bge_large_en_v15/results_reranker_bge — пересобранные реранкером чанки, найденные изначально bge large en v1.5.

20) В in_notebooks/01_parse_and_chunk.ipynb содержатся исследования по модели e5-large-v2, а также код для сравнения результатов e5-large-v2 и bge large en v1.5, и код для генерации графиков.

21) В in_notebooks/bge-large-en-v-poltara.ipynb содержатся исследования по модели bge large en v1.5.