program fibonacci
  implicit none
  integer :: n, a, b, temp, i

  ! Read input
  read *, n

  ! Calculate Fibonacci
  if (n <= 0) then
    print *, 0
  else if (n == 1) then
    print *, 1
  else
    a = 0
    b = 1
    do i = 2, n
      temp = a + b
      a = b
      b = temp
    end do
    print *, b
  end if

end program fibonacci