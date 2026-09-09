program is_prime
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Check if prime
  result = .true.
  if (n <= 1) result = .false.
  if (n == 2) result = .true.
  if (n == 3) result = .true.
  if (n > 3 .and. mod(n, 2) == 0) result = .false.
  if (n > 3) then
    integer :: i
    do i = 3, sqrt(real(n), kind=real(0))
      if (mod(n, i) == 0) then
        result = .false.
        exit
      end if
    end do
  end if

  ! Output result
  print *, result
end program is_prime