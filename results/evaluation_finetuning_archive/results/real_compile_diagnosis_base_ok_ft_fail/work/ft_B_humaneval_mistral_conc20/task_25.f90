program factorize
  implicit none
  integer :: n, i, factor
  integer, allocatable :: factors(:)
  integer :: count

  ! Read input
  read *, n

  ! Find prime factors
  count = 0
  i = 2
  do while (i * i <= n)
    do while (mod(n, i) == 0)
      count = count + 1
      n = n / i
    end do
    i = i + 1
  end do
  if (n > 1) then
    count = count + 1
  end if

  ! Allocate array for factors
  allocate(factors(count))

  ! Store factors
  i = 2
  do while (i * i <= n)
    do while (mod(n, i) == 0)
      factors(i) = i
      n = n / i
    end do
    i = i + 1
  end do
  if (n > 1) then
    factors(count) = n
  end if

  ! Output factors
  do i = 1, count
    print *, factors(i)
  end do

end program factorize