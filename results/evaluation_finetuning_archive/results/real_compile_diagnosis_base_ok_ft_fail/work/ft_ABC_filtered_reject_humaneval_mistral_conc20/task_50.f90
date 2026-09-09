program main
  implicit none
  character(len=3) :: s
  character(len=3) :: result
  
  ! Read input
  read(*, '(a)') s
  
  ! Call decode_shift
  result = decode_shift(s)
  
  ! Print output
  write(*, '(a)') result
end program main