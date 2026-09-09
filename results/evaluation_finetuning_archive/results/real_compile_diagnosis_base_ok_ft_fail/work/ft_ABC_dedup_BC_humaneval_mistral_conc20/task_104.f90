program main
  implicit none
  integer, parameter :: max_len = 100
  integer :: x_len
  integer :: x(max_len)
  integer :: y(max_len)
  integer :: y_len
  integer :: i, j, k
  integer :: temp

  ! Read input
  read(*,*) x_len
  read(*,*) (x(i), i=1,x_len)

  ! Initialize y_len
  y_len = 0

  ! Process each element
  do i = 1, x_len
    if (contains_even_digit(x(i))) then
      y_len = y_len + 1
      y(y_len) = x(i)
    end if
  end do

  ! Sort y array
  do i = 1, y_len
    do j = i+1, y_len
      if (y(i) > y(j)) then
        temp = y(i)
        y(i) = y(j)
        y(j) = temp
      end if
    end do
  end do

  ! Output result
  print *, (y(i), i=1,y_len)

contains

  logical function contains_even_digit(n)
    integer, intent(in) :: n
    integer :: digit
    contains_even_digit = .false.
    do while (n > 0)
      digit = mod(n, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        contains_even_digit = .true.
        return
      end if
      n = n / 10
    end do
  end function contains_even_digit

end program main