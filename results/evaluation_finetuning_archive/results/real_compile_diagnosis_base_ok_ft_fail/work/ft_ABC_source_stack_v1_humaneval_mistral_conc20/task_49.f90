program modp
  implicit none
  integer :: n, p, result, i

  read *, n
  read *, p

  result = 1
  do i = 1, n
    result = mod(result * 2, p)
  end do

  print *, result
end program modp