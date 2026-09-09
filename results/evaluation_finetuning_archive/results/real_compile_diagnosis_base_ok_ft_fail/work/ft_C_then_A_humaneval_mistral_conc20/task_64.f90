program vowels_count
  implicit none
  character(len=100) :: input
  integer :: result
  read (*, '(a)') input
  result = vowels_count(input)
  print *, result
end program vowels_count