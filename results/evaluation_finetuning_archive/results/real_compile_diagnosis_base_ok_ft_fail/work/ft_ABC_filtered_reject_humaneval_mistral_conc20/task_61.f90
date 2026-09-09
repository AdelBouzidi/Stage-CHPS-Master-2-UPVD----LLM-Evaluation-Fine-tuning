program main
  implicit none
  character(len=100) :: brackets
  logical :: result

  ! Read input from stdin
  read(*, '(A)') brackets

  ! Call the function
  result = correct_bracketing(brackets)

  ! Print output
  print *, result
end program main