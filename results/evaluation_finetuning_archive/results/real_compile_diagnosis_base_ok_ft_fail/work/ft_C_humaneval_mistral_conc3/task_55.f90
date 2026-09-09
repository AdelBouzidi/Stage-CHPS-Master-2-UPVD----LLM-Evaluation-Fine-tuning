program fibonacci
  implicit none
  integer :: n, a, b, temp, result

  ! Read input
  read(*, *) n

  ! Calculate Fibonacci number
  if (n <= 0) then
    result = 0
  else if (n == 1) then
    result = 1
  else if (n == 2) then
    result = 1
  else
    a = 1
    b = 1
    do i = 3, n
      temp = a + b
      a = b
      b = temp
    end do
    result = b
  end if

  ! Output result
  print *, result
end program fibonacci