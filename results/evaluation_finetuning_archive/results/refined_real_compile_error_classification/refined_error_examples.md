# Refined error examples


## compiled_but_wrong_answer

### ft_ABC_Strong_humaneval_mistral_conc20 / task 24

- ft_status: `ineq`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 77

- ft_status: `ineq`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 24

- ft_status: `ineq`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 76

- ft_status: `ineq`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 18

- ft_status: `ineq`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```


## intent_in_modified

### ft_ABC_Strong_humaneval_mistral_conc20 / task 25

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_25.f90:35:8:

   35 |         n = n / i
      |        1
Error: Dummy argument ‘n’ with INTENT(IN) in variable definition context (assignment) at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 59

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_59.f90:23:8:

   23 |         n = n / i
      |        1
Error: Dummy argument ‘n’ with INTENT(IN) in variable definition context (assignment) at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 104

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_104.f90:71:6:

   71 |       val = val / 10
      |      1
Error: Dummy argument ‘val’ with INTENT(IN) in variable definition context (assignment) at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 25

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_25.f90:34:8:

   34 |         n = n / i
      |        1
Error: Dummy argument ‘n’ with INTENT(IN) in variable definition context (assignment) at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 59

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_59.f90:23:8:

   23 |         n = n / i
      |        1
Error: Dummy argument ‘n’ with INTENT(IN) in variable definition context (assignment) at (1)

```


## compiled_ok_other_failure

### ft_ABC_Strong_humaneval_mistral_conc20 / task 55

- ft_status: `ok`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 76

- ft_status: `ok`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 20

- ft_status: `ok`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 55

- ft_status: `ok`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 102

- ft_status: `ok`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```


## undeclared_variable

### ft_ABC_Strong_humaneval_mistral_conc20 / task 121

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_121.f90:15:6:

   15 |   do i = 1, lst_len
      |      1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 55

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_55.f90:28:10:

   28 |       do i = 2, n
      |          1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 121

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_121.f90:15:6:

   15 |   do i = 1, lst_len
      |      1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 100

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_dedup_BC_humaneval_mistral_conc20/task_100.f90:14:8:

   14 |     do i = 3, n
      |        1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 20

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_20.f90:23:10:

   23 |       diff = abs(numbers(i) - numbers(j))
      |          1
Error: Symbol ‘diff’ at (1) has no IMPLICIT type

```


## empty_code_or_no_program

### ft_ABC_Strong_humaneval_mistral_conc20 / task 100

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `empty_or_no_program`

```text
/usr/bin/ld: /usr/lib/gcc/aarch64-linux-gnu/14/../../../aarch64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1c): undefined reference to `main'
/usr/bin/ld: (.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 131

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `empty_or_no_program`

```text
/usr/bin/ld: /usr/lib/gcc/aarch64-linux-gnu/14/../../../aarch64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1c): undefined reference to `main'
/usr/bin/ld: (.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 83

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `empty_or_no_program`

```text
/usr/bin/ld: /usr/lib/gcc/aarch64-linux-gnu/14/../../../aarch64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1c): undefined reference to `main'
/usr/bin/ld: (.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 100

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `empty_or_no_program`

```text
/usr/bin/ld: /usr/lib/gcc/aarch64-linux-gnu/14/../../../aarch64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1c): undefined reference to `main'
/usr/bin/ld: (.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 131

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `empty_or_no_program`

```text
/usr/bin/ld: /usr/lib/gcc/aarch64-linux-gnu/14/../../../aarch64-linux-gnu/Scrt1.o: in function `_start':
(.text+0x1c): undefined reference to `main'
/usr/bin/ld: (.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status

```


## compiled_but_runtime_error

### ft_ABC_Strong_humaneval_mistral_conc20 / task 50

- ft_status: `runtime_err`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_50.f90:5:19:

    5 |   read *, input_str
      |                   ^
Warning: ‘.input_str’ may be used uninitialized [-Wmaybe-uninitialized]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_50.f90:29:29:

   29 |   end subroutine decode_shift
      |                             ^
note: ‘.input_str’ was declared here

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 21

- ft_status: `runtime_err`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_21.f90:45:8:

   45 |     if (range == 0.0_rk) then
      |        1
Warning: Equality comparison for REAL(8) at (1) [-Wcompare-reals]

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 50

- ft_status: `runtime_err`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_50.f90:5:19:

    5 |   read *, input_str
      |                   ^
Warning: ‘.input_str’ may be used uninitialized [-Wmaybe-uninitialized]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_50.f90:29:29:

   29 |   end subroutine decode_shift
      |                             ^
note: ‘.input_str’ was declared here

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 21

- ft_status: `runtime_err`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:38:8:

   38 |     if (max_val == min_val) then
      |        1
Warning: Equality comparison for REAL(8) at (1) [-Wcompare-reals]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:19:19:

   19 |     print *, res(i)
      |                   ^
Warning: ‘res.dim[0].lbound’ may be used uninitialized [-Wmaybe-uninitialized]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:6:33:

    6 |   real(dp), allocatable :: res(:)
      |                                 ^
note: ‘res’ declared here
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:19:12:

   19 |     print *, res(i)
      |            ^
Warning: ‘res.dim[0].lbound’ may be used uninitialized [-Wmaybe-uninitialized]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:6:33:

    6 |   real(dp), allocatable :: res(:)
      |                                 ^
note: ‘res’ declared here
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:19:19:

   19 |     print *, res(i)
      |                   ^
Warning: ‘res.dim[0].ubound’ may be used uninitialized [-Wmaybe-uninitialized]
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_21.f90:6:33:

    6 |   real(dp), al
...[TRUNCATED]...
```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 73

- ft_status: `runtime_err`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```


## compile_other

### ft_ABC_Strong_humaneval_mistral_conc3 / task 123

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `compile_other`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_123.f90:39:41:

   39 |   function sort_array(arr) result(sorted)
      |                                         1
Error: Array ‘sorted’ at (1) cannot have a deferred shape
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_123.f90:25:25:

   25 |         allocate(odd_nums(size(odd_nums) + 1))
      |                         1
Error: ‘odd_nums’ must not appear in the array specification at (1) in the same ALLOCATE statement where it is itself allocated

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 155

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `compile_other`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_155.f90:22:16:

   22 |     if (mod(int(digit(i:i)), 2) == 0) then
      |                1
Error: ‘a’ argument of ‘int’ intrinsic at (1) must have a numeric type

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 31

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `compile_other`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_31.f90:31:51:

   31 |       do i = 3, int(sqrt(real(n, kind=real(0, kind=n))))
      |                                                   1
Error: Parameter ‘n’ at (1) has not been declared or is a variable, which does not reduce to a constant expression
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_31.f90:31:51:

   31 |       do i = 3, int(sqrt(real(n, kind=real(0, kind=n))))
      |                                                   1
Error: ‘kind’ argument of ‘real’ intrinsic at (1) must be a constant

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 106

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `compile_other`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_106.f90:41:15:

   18 |       result(i) = sum_to(i)
      |                  2
......
   41 |     do i = 1, k
      |               1
Error: Index variable ‘i’ redefined at (1) in procedure ‘sum_to’ called from within DO loop at (2)

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 123

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `compile_other`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_123.f90:24:17:

   24 |     odd_nums = []
      |                 1
Error: Empty array constructor at (1) is not allowed

```


## assumed_length_character_local

### ft_ABC_Strong_humaneval_mistral_conc20 / task 18

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_18.f90:3:25:

    3 |   character(len=*) :: str, sub
      |                         1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_18.f90:3:30:

    3 |   character(len=*) :: str, sub
      |                              1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 64

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_64.f90:3:31:

    3 |   character(len=*) :: input_str
      |                               1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 64

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_64.f90:3:31:

    3 |   character(len=*) :: input_str
      |                               1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 18

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_18.f90:3:28:

    3 |   character(len=*) :: string, substring
      |                            1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_18.f90:3:39:

    3 |   character(len=*) :: string, substring
      |                                       1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER

```

### ft_AB_antineighbor_humaneval_mistral_conc20 / task 64

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `intent_in_modified`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_antineighbor_humaneval_mistral_conc20/task_64.f90:3:41:

    3 |   character(len=*), dimension(1) :: input
      |                                         1
Error: Entity with assumed character length at (1) must be a dummy argument or a PARAMETER

```


## invalid_operator_or_expression

### ft_ABC_Strong_humaneval_mistral_conc20 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `invalid_operator_or_expression`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_49.f90:21:7:

   21 |       result = (result * 2) mod p
      |       1
Error: Unclassifiable statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `invalid_operator_or_expression`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_49.f90:21:7:

   21 |       result = (result * 2) mod p
      |       1
Error: Unclassifiable statement at (1)

```

### ft_ABC_dedup_BC_humaneval_mistral_conc20 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `invalid_operator_or_expression`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_dedup_BC_humaneval_mistral_conc20/task_49.f90:22:7:

   22 |       result = (result * 2) mod p
      |       1
Error: Unclassifiable statement at (1)

```

### ft_ABC_filtered_accept_humaneval_mistral_conc20 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `invalid_operator_or_expression`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_accept_humaneval_mistral_conc20/task_49.f90:25:7:

   25 |       res = (res * 2) mod p
      |       1
Error: Unclassifiable statement at (1)

```

### ft_ABC_source_burkardt_humaneval_mistral_conc20 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `invalid_operator_or_expression`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_burkardt_humaneval_mistral_conc20/task_49.f90:23:7:

   23 |       res = (res * 2) mod p
      |       1
Error: Unclassifiable statement at (1)

```


## syntax_error_other

### ft_ABC_Strong_humaneval_mistral_conc20 / task 106

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_106.f90:18:24:

   18 |       result(i) = sum(1:i)
      |                        1
Error: Syntax error in argument list at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 106

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_106.f90:18:24:

   18 |       result(i) = sum(1:i)
      |                        1
Error: Syntax error in argument list at (1)

```

### ft_ABC_source_numericalhub_humaneval_mistral_conc20 / task 106

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_numericalhub_humaneval_mistral_conc20/task_106.f90:14:24:

   14 |       result(i) = sum(1:i)
      |                        1
Error: Syntax error in argument list at (1)

```

### ft_B_humaneval_mistral_conc20 / task 2

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_2.f90:7:8:

    7 |   write *, result
      |        1
Error: Syntax error in WRITE statement at (1)

```

### ft_B_humaneval_mistral_conc20 / task 49

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_49.f90:11:8:

   11 |   write *, result
      |        1
Error: Syntax error in WRITE statement at (1)

```


## print_parentheses_syntax

### ft_ABC_Strong_humaneval_mistral_conc20 / task 2

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_2.f90:12:8:

   12 |   print(*,*) result
      |        1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 41

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_41.f90:12:8:

   12 |   print(*,*) result
      |        1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 53

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_53.f90:12:8:

   12 |   print(*,*) result
      |        1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 102

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_102.f90:13:8:

   13 |   print(*,*) result
      |        1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 2

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_2.f90:12:8:

   12 |   print(*,*) result
      |        1
Error: Syntax error in PRINT statement at (1)

```


## type_mismatch_or_intrinsic_misuse

### ft_ABC_Strong_humaneval_mistral_conc20 / task 155

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `type_mismatch`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_155.f90:17:25:

   17 |     digit = trim(adjustl(num))
      |                         1
Error: In call to ‘adjustl’ at (1), type mismatch in argument ‘string’; pass ‘INTEGER(4)’ to ‘CHARACTER(*,0)’
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_155.f90:19:27:

   19 |       digit = trim(adjustl(num))
      |                           1
Error: In call to ‘adjustl’ at (1), type mismatch in argument ‘string’; pass ‘INTEGER(4)’ to ‘CHARACTER(*,0)’
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_155.f90:22:27:

   22 |       digit = trim(adjustl(num))
      |                           1
Error: In call to ‘adjustl’ at (1), type mismatch in argument ‘string’; pass ‘INTEGER(4)’ to ‘CHARACTER(*,0)’
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_155.f90:16:37:

   16 |   do i = 1, len_trim(adjustl(adjustl(num)))
      |                                     1
Error: In call to ‘adjustl’ at (1), type mismatch in argument ‘string’; pass ‘INTEGER(4)’ to ‘CHARACTER(*,0)’
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_155.f90:28:25:

   28 |     digit = trim(adjustl(num))
      |                         1
Error: In call to ‘adjustl’ at (1), type mismatch in argument ‘string’; pass ‘INTEGER(4)’ to ‘CHARACTER(*,0)’
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/t
...[TRUNCATED]...
```

### ft_ABC_source_fortran_lang_humaneval_mistral_conc20 / task 76

- ft_status: `ok`
- compiled_ok: `False`
- old compile_primary: `type_mismatch`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:13:21:

   13 |             result = .true.
      |                     1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:15:21:

   15 |             result = .false.
      |                     1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:19:21:

   19 |             result = .true.
      |                     1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:21:21:

   21 |             result = .false.
      |                     1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:24:17:

   24 |         result = .true.
      |                 1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:28:21:

   28 |             result = .false.
      |                     1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_fortran_lang_humaneval_mistral_conc20/task_76.f90:30:21:

   30 |          
...[TRUNCATED]...
```

### ft_AB_shuffle_humaneval_mistral_conc20 / task 155

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `type_mismatch`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_shuffle_humaneval_mistral_conc20/task_155.f90:16:16:

   16 |         digit = mod(num, 10)
      |                1
Error: Cannot convert INTEGER(4) to CHARACTER(1) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_shuffle_humaneval_mistral_conc20/task_155.f90:17:12:

   17 |         if (digit /= 0) then
      |            1
Error: Operands of comparison operator ‘/=’ at (1) are CHARACTER(1)/INTEGER(4)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_shuffle_humaneval_mistral_conc20/task_155.f90:18:20:

   18 |             if (mod(digit, 2) == 0) then
      |                    1
Error: ‘a’ argument of ‘mod’ intrinsic at (1) must be INTEGER or REAL

```

### ft_AB_shuffle_humaneval_mistral_conc3 / task 155

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `type_mismatch`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_shuffle_humaneval_mistral_conc3/task_155.f90:20:12:

   20 |     digit = mod(num, 10)
      |            1
Error: Cannot convert INTEGER(4) to CHARACTER(1) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_shuffle_humaneval_mistral_conc3/task_155.f90:21:12:

   21 |     if (mod(digit, 2) == 0) then
      |            1
Error: ‘a’ argument of ‘mod’ intrinsic at (1) must be INTEGER or REAL

```

### ft_B_humaneval_mistral_conc20 / task 76

- ft_status: `ineq`
- compiled_ok: `False`
- old compile_primary: `type_mismatch`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_76.f90:8:13:

    8 |     result = .false.
      |             1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_76.f90:10:13:

   10 |     result = .false.
      |             1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_76.f90:12:13:

   12 |     result = .true.
      |             1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_76.f90:14:13:

   14 |     result = .true.
      |             1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_humaneval_mistral_conc20/task_76.f90:19:13:

   19 |     result = .false.
      |             1
Error: Cannot convert LOGICAL(4) to INTEGER(4) at (1)

```


## declaration_after_executable

### ft_ABC_Strong_humaneval_mistral_conc3 / task 71

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_71.f90:16:13:

   16 |     real :: s
      |             1
Error: Unexpected data declaration statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_71.f90:17:5:

   17 |     s = (a + b + c) / 2.0
      |     1
Error: Symbol ‘s’ at (1) has no IMPLICIT type

```

### ft_ABC_filtered_reject_humaneval_mistral_conc20 / task 21

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_reject_humaneval_mistral_conc20/task_21.f90:15:30:

   15 |   real(dp) :: min_val, max_val
      |                              1
Error: Unexpected data declaration statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_reject_humaneval_mistral_conc20/task_21.f90:17:9:

   17 |   max_val = numbers(1)
      |         1
Error: Symbol ‘max_val’ at (1) has no IMPLICIT type
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_filtered_reject_humaneval_mistral_conc20/task_21.f90:16:9:

   16 |   min_val = numbers(1)
      |         1
Error: Symbol ‘min_val’ at (1) has no IMPLICIT type

```

### ft_AB_antineighbor_humaneval_mistral_conc20 / task 20

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_antineighbor_humaneval_mistral_conc20/task_20.f90:23:22:

   23 |       real(dp) :: diff
      |                      1
Error: Unexpected data declaration statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AB_antineighbor_humaneval_mistral_conc20/task_20.f90:24:10:

   24 |       diff = abs(numbers(i) - numbers(j))
      |          1
Error: Symbol ‘diff’ at (1) has no IMPLICIT type

```

### ft_AC_antineighbor_humaneval_mistral_conc3 / task 20

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc3/task_20.f90:23:22:

   23 |       real(dp) :: diff
      |                      1
Error: Unexpected data declaration statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc3/task_20.f90:24:10:

   24 |       diff = abs(numbers(i) - numbers(j))
      |          1
Error: Symbol ‘diff’ at (1) has no IMPLICIT type

```

### ft_A_ep2_humaneval_mistral_conc20 / task 73

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_A_ep2_humaneval_mistral_conc20/task_73.f90:15:14:

   15 |   integer :: i
      |              1
Error: Unexpected data declaration statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_A_ep2_humaneval_mistral_conc20/task_73.f90:16:6:

   16 |   do i = 1, arr_len/2
      |      1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```


## print_statement_syntax

### ft_ABC_Strong_humaneval_mistral_conc20 / task 45

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_45.f90:13:8:

   13 |   print(*,'(F6.1)') area
      |        1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 71

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_71.f90:16:10:

   16 |     print(*,'(F6.2)') area
      |          1
Error: Syntax error in PRINT statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_71.f90:18:10:

   18 |     print(*,'(I6)') -1
      |          1
Error: Syntax error in PRINT statement at (1)

```

### ft_ABC_Strong_humaneval_mistral_conc20 / task 123

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_123.f90:13:8:

   13 |   print(*,'(i0)') result
      |        1
Error: Syntax error in PRINT statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_123.f90:26:25:

   26 |         allocate(temp_arr(size(temp_arr)+1))
      |                         1
Error: ‘temp_arr’ must not appear in the array specification at (1) in the same ALLOCATE statement where it is itself allocated

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 73

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_73.f90:22:8:

   22 |   print(*,'(i0)') result
      |        1
Error: Syntax error in PRINT statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_73.f90:15:6:

   15 |   do i = 1, arr_len/2
      |      1
Error: Symbol ‘i’ at (1) has no IMPLICIT type

```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 159

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_159.f90:19:8:

   19 |   print(*,'(2I8)') result
      |        1
Error: Syntax error in PRINT statement at (1)

```


## compiled_but_evaluator_exception

### ft_ABC_source_burkardt_humaneval_mistral_conc20 / task 123

- ft_status: `exception`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_ABC_source_numerical_methods_humaneval_mistral_conc20 / task 50

- ft_status: `exception`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_AB_shuffle_humaneval_mistral_conc20 / task 59

- ft_status: `exception`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```

### ft_AB_shuffle_humaneval_mistral_conc3 / task 59

- ft_status: `exception`
- compiled_ok: `True`
- old compile_primary: `compile_ok`

```text

```


## allocatable_or_shape_error

### ft_ABC_source_stack_v2_humaneval_mistral_conc20 / task 123

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `allocatable_shape_or_allocate`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_source_stack_v2_humaneval_mistral_conc20/task_123.f90:40:13:

   40 |     allocate(result(count))
      |             1
Error: Allocate-object at (1) must be ALLOCATABLE or a POINTER

```

### ft_AC_antineighbor_humaneval_mistral_conc20 / task 104

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `allocatable_shape_or_allocate`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc20/task_104.f90:64:35:

   64 |   function sort(arr) result(sorted)
      |                                   1
Error: Array ‘sorted’ at (1) cannot have a deferred shape
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc20/task_104.f90:34:20:

   34 |       do j = 1, len(x(i))
      |                    1
Error: ‘string’ argument of ‘len’ intrinsic at (1) must be CHARACTER
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc20/task_104.f90:45:13:

   45 |     allocate(result(n))
      |             1
Error: Allocate-object at (1) must be ALLOCATABLE or a POINTER
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_AC_antineighbor_humaneval_mistral_conc20/task_104.f90:49:20:

   49 |       do j = 1, len(x(i))
      |                    1
Error: ‘string’ argument of ‘len’ intrinsic at (1) must be CHARACTER

```

### ft_A_half1_humaneval_mistral_conc20 / task 100

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `allocatable_shape_or_allocate`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_A_half1_humaneval_mistral_conc20/task_100.f90:22:13:

   22 |     allocate(result(n))
      |             1
Error: Allocate-object at (1) must be ALLOCATABLE or a POINTER

```


## bad_contains_or_program_structure

### ft_B_then_A_humaneval_mistral_conc20 / task 131

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:3:21:

    3 |     integer function digits(n)
      |                     1
Error: Syntax error in data declaration at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:5:11:

    5 |     digits = 0
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:7:11:

    7 |     digits = 0
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:9:11:

    9 |     digits = 1
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:11:11:

   11 |     digits = digits * mod(n, 10)
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:15:7:

   15 |     end function digits
      |       1
Error: Expecting END PROGRAM statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:16:16:

   16 |     program main
      |                1
Error: Unexpected PROGRAM statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc20/task_131.f90:17:16:

   17 |     integer :: n
      |                1
Error: Symbol ‘n’ 
...[TRUNCATED]...
```

### ft_B_then_A_humaneval_mistral_conc3 / task 131

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:3:21:

    3 |     integer function digits(n)
      |                     1
Error: Syntax error in data declaration at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:5:11:

    5 |     digits = 0
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:7:11:

    7 |     digits = 0
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:9:11:

    9 |     digits = 1
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:11:11:

   11 |     digits = digits * mod(n, 10)
      |           1
Error: ‘digits’ at (1) is not a variable
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:15:7:

   15 |     end function digits
      |       1
Error: Expecting END PROGRAM statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:16:16:

   16 |     program main
      |                1
Error: Unexpected PROGRAM statement at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_131.f90:17:16:

   17 |     integer :: n
      |                1
Error: Symbol ‘n’ at (1) a
...[TRUNCATED]...
```

### ft_B_then_A_humaneval_mistral_conc3 / task 138

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `syntax_error`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:6:36:

    6 |       result = is_equal_to_sum_even(n)
      |                                    1
Error: Symbol at (1) is not appropriate for an expression
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:9:46:

    9 |       logical function is_equal_to_sum_even(n)
      |                                              1
Error: PROGRAM attribute of ‘is_equal_to_sum_even’ conflicts with PROCEDURE attribute at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:10:45:

   10 |         if (mod(n, 2) == 0 .and. n >= 8) then
      |                                             1
Error: Unexpected block IF statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:11:32:

   11 |            is_equal_to_sum_even = .true.
      |                                1
Error: Symbol ‘is_equal_to_sum_even’ at (1) has already been host associated
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:12:12:

   12 |         else
      |            1
Error: Unexpected ELSE statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_B_then_A_humaneval_mistral_conc3/task_138.f90:13:32:

   13 |            is_equal_to_sum_even = .false.
      |                                1
Error: Symbol ‘is_equal_to_sum_even’ at (1) has already been ho
...[TRUNCATED]...
```


## c_like_procedure_signature

### ft_ABC_Strong_humaneval_mistral_conc20 / task 20

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:21:39:

   21 |   subroutine find_closest_elements(int numbers_len, float[] numbers)
      |                                       1
Error: Unexpected junk in formal argument list at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:22:38:

   22 |     integer, intent(in) :: numbers_len
      |                                      1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:23:38:

   23 |     real(dp), intent(in) :: numbers(:)
      |                                      1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:24:45:

   24 |     real(dp), intent(out) :: result1, result2
      |                                             1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:25:35:

   25 |     integer :: i, j, min_idx, min_j
      |                                   1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc20/task_20.f90:26:30:

   26 |     real(dp) :: min_diff, diff
      |                              1
Error
...[TRUNCATED]...
```

### ft_ABC_Strong_humaneval_mistral_conc3 / task 20

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `c_like_signature_or_invalid_decl`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:21:39:

   21 |   subroutine find_closest_elements(int numbers_len, float numbers, float result1, float result2)
      |                                       1
Error: Unexpected junk in formal argument list at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:22:17:

   22 |     implicit none
      |                 1
Error: Unexpected IMPLICIT NONE statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:23:38:

   23 |     integer, intent(in) :: numbers_len
      |                                      1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:24:38:

   24 |     real(dp), intent(in) :: numbers(:)
      |                                      1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:25:45:

   25 |     real(dp), intent(out) :: result1, result2
      |                                             1
Error: Unexpected data declaration statement in CONTAINS section at (1)
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_20.f90:26:35:

   26 |     integer :: i, j, min_idx, min_j
      |                                   1
Error: Unexp
...[TRUNCATED]...
```


## missing_iso_fortran_env_kind

### ft_ABC_Strong_humaneval_mistral_conc3 / task 31

- ft_status: `compile_err`
- compiled_ok: `False`
- old compile_primary: `implicit_declaration`

```text
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_31.f90:30:40:

   30 |       do i = 3, sqrt(real(n, kind=real32)), 2
      |                                        1
Error: Symbol ‘real32’ at (1) has no IMPLICIT type
results/real_compile_diagnosis_base_ok_ft_fail/work/ft_ABC_Strong_humaneval_mistral_conc3/task_31.f90:30:40:

   30 |       do i = 3, sqrt(real(n, kind=real32)), 2
      |                                        1
Error: Symbol ‘real32’ at (1) has no IMPLICIT type

```

