program main
  implicit none
  character(len=100) :: brackets
  logical :: result
  read *, brackets
  result = correct_bracketing(brackets)
  print *, result
end program main