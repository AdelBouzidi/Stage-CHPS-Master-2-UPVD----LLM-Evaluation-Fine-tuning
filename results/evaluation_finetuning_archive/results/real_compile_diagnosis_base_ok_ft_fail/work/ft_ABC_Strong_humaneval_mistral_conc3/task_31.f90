program is_prime_demo
  implicit none
  integer :: n
  logical :: result

  ! Read input from stdin
  read(*,*) n

  ! Call the is_prime function
  result = is_prime(n)

  ! Write output to stdout
  print *, result

contains

  logical function is_prime(n)
    integer, intent(in) :: n
    integer :: i
    logical :: prime

    if (n <= 1) then
      prime = .false.
    else if (n == 2) then
      prime = .true.
    else if (mod(n, 2) == 0) then
      prime = .false.
    else
      prime = .true.
      do i = 3, sqrt(real(n, kind=real32)), 2
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if

    is_prime = prime
  end function is_prime

end program is_prime_demo