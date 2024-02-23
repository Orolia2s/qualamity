## Static analysis report

28 violations identified:

| Name | Location | Details |
| :-- | :-- | :-- |
| Definition de variables dans un header | `include/bad_header.h:5:12` | La constante `some_global_array` est définie dans un header |
| Definition de variables dans un header | `include/bad_header.h:6:11` | La constante `some_global` est définie dans un header |
| Definition de variables dans un header | `include/middle_header.h:5:18` | La constante `answer` est définie dans un header |
| Documenter l'ensemble des declarations top-level | `include/bad_header.h:5` | La variable `some_global_array` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `include/bad_header.h:6` | La variable `some_global` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `include/bad_header.h:8` | La fonction `defined_in_header` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/abs.c:5` | La fonction `abs` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/abs.c:10` | La fonction `time` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/abs.c:15` | La fonction `strtoi` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/ko.c:3` | L'énumération `cardinal` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/ko.c:10` | La fonction `name` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/ko.c:21` | La fonction `cardinal_to_string` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/main.c:9` | La fonction `isdigit` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/main.c:14` | La fonction `main` n'est pas documentée |
| Documenter l'ensemble des declarations top-level | `src/main.c:21` | La fonction `do_something` n'est pas documentée |
| Implementation de fonctions dans un header | `include/bad_header.h:8:5` | La fonction `defined_in_header` est définie dans un header |
| Implementation de fonctions dans un header | `include/middle_header.h:7:14` | La fonction `square_root` est définie dans un header |
| Ne pas laisser de TODOs | `src/abs.c:7:27` | à faire: `Todo: Use libc` |
| Ne pas laisser de TODOs | `src/main.c:28:14` | à faire: `TODO: handle cleanly` |
| Ne pas redéfinir les fonctions standards | `src/abs.c:5:5` | Redéfinition de la fonction `abs` |
| Ne pas redéfinir les fonctions standards | `src/abs.c:10:13` | Redéfinition de la fonction `time` |
| Ne pas redéfinir les fonctions standards | `src/main.c:9:5` | Redéfinition de la fonction `isdigit` |
| Utilisation de abort ou _Exit | `src/main.c:28:3` | La fonction `abort` est appelée |
| Utilisation de abort ou _Exit | `src/main.c:31:2` | La fonction `_Exit` est appelée |
| Utilisation de atoi et dérivées | `src/abs.c:17:9` | La fonction `atoi` est appelée |
| Utilisation de system ou getenv | `src/abs.c:12:22` | La fonction `system` est appelée |
| Utilisation de system ou getenv | `src/main.c:26:3` | La fonction `getenv` est appelée |
| Utilisation de system ou getenv | `src/main.c:27:3` | La fonction `system` est appelée |
