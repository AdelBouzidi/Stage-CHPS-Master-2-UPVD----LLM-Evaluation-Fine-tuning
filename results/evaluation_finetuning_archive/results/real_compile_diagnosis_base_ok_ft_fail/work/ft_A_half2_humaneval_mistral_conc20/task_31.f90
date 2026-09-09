program main
  implicit none
  integer :: n
  logical :: result

  ! Read input
  read(*,*) n

  ! Call the function
  result = is_prime(n)

  ! Print output
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
      do i = 3, sqrt(real(n, kind=real(0.0)))
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if

    is_prime = prime
  end function is_prime

end program main