program main
  implicit none
  integer :: num
  integer :: even_count, odd_count

  ! Read input
  read(*, *) num

  ! Call the function
  call even_odd_count(num, even_count, odd_count)

  ! Print output
  print *, even_count, odd_count
end program main