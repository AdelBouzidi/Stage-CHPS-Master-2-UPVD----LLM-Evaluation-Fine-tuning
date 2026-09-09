program x_or_y
  implicit none
  integer :: n, x, y
  integer :: result

  ! Read input values
  read(*,*) n
  read(*,*) x
  read(*,*) y

  ! Call the function
  result = x_or_y(n, x, y)

  ! Output the result
  print *, result

contains

  function x_or_y(n, x, y) result(res)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: res
    integer :: i

    ! Check if n is prime
    if (is_prime(n)) then
      res = x
    else
      res = y
    end if
  end function x_or_y

  function is_prime(n) result(prime)
    implicit none
    integer, intent(in) :: n
    logical :: prime
    integer :: i

    if (n <= 1) then
      prime = .false.
    else if (n == 2) then
      prime = .true.
    else if (mod(n, 2) == 0) then
      prime = .false.
    else
      prime = .true.
      do i = 3, int(sqrt(real(n))) + 1, 2
        if (mod(n, i) == 0) then
          prime = .false.
          exit
        end if
      end do
    end if
  end function is_prime

end program x_or_y