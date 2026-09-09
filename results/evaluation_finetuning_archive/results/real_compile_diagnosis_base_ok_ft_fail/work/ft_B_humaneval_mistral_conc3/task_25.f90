program factorize
  implicit none
  integer :: n, i
  integer, allocatable :: factors(:)
  integer :: count

  ! Read input
  read *, n

  ! Initialize factors array
  count = 0
  allocate(factors(100))

  ! Find prime factors
  i = 2
  do while (i * i <= n)
    do while (mod(n, i) == 0)
      count = count + 1
      factors(count) = i
      n = n / i
    end do
    i = i + 1
  end do

  ! If n > 1, then the remaining n is a prime factor
  if (n > 1) then
    count = count + 1
    factors(count) = n
  end if

  ! Resize array to actual size
  deallocate(factors)
  allocate(factors(count))

  ! Output factors
  do i = 1, count
    write (*, *) factors(i)
  end do

end program factorize