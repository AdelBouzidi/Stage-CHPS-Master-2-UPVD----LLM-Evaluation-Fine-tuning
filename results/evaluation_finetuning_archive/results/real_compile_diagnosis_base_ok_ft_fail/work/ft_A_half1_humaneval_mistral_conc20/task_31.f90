program main
  implicit none
  integer :: n
  logical :: result

  ! Read input from stdin
  read(*,*) n

  ! Call the is_prime function
  result = is_prime(n)

  ! Output the result
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
      do i = 3, sqrt(real(n)), 2
        if (mod(n, i) == 0) then
          is_prime = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program main