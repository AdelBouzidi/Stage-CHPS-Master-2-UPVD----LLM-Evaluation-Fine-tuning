program collatz_odd
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n

  ! Initialize result array
  allocate(result(n))
  i = 0

  ! Generate Collatz sequence and collect odd numbers
  do while (n /= 1)
    if (mod(n, 2) /= 0) then
      i = i + 1
      result(i) = n
    end if
    if (mod(n, 2) == 0) then
      n = n / 2
    else
      n = 3 * n + 1
    end if
  end do

  ! Add the final 1 if it's odd (it always is)
  i = i + 1
  result(i) = 1

  ! Output result
  write(*,*) result

end program collatz_odd