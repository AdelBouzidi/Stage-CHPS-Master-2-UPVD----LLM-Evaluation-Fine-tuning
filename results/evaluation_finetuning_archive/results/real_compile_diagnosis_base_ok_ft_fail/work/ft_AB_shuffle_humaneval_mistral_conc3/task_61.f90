program main
  implicit none
  character(len=100) :: brackets
  logical :: result

  ! Read input from stdin
  read(*, '(a)') brackets

  ! Call the function
  result = correct_bracketing(brackets)

  ! Output the result
  print *, result
end program main