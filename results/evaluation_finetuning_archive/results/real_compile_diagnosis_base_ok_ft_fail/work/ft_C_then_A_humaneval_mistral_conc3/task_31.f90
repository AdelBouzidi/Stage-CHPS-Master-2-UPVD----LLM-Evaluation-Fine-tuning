program is_prime_demo
  implicit none
  integer :: n
  logical :: result

  ! Read input number from stdin
  read(*,*) n

  ! Check if number is prime
  result = is_prime(n)

  ! Output result
  print *, result

contains

  logical function is_prime(n)
    integer, intent(in) :: n
    integer :: i

    if (n <= 1) then
      is_prime = .false.
    else if (n == 2) then
      is_prime = .true.
    else if (mod(n, 2) == 0) then
      is_prime = .false.
    else
      is_prime = .true.
      do i = 3, int(sqrt(real(n))) + 1, 2
        if (mod(n, i) == 0) then
          is_prime = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program is_prime_demo