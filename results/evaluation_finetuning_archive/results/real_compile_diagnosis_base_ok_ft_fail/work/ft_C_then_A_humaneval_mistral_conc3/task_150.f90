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

  integer function x_or_y(n, x, y)
    implicit none
    integer, intent(in) :: n, x, y
    integer :: i
    logical :: is_prime

    is_prime = .true.
    if (n < 2) then
      is_prime = .false.
    else
      do i = 2, n-1
        if (mod(n, i) == 0) then
          is_prime = .false.
          exit
        end if
      end do
    end if

    if (is_prime) then
      x_or_y = x
    else
      x_or_y = y
    end if
  end function x_or_y

end program x_or_y