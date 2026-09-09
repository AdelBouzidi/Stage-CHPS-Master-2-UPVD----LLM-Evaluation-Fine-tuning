program main
  implicit none
  integer, parameter :: max_len = 100
  integer :: x_len
  integer :: x(max_len)
  integer :: result(max_len)
  integer :: n
  integer :: i, j, k
  integer :: temp

  ! Read input
  read(*,*) x_len
  read(*,*) (x(i), i=1,x_len)

  ! Initialize result array
  n = 0
  do i = 1, x_len
    if (no_even_digit(x(i))) then
      n = n + 1
      result(n) = x(i)
    end if
  end do

  ! Sort result array
  do i = 1, n-1
    do j = i+1, n
      if (result(i) > result(j)) then
        temp = result(i)
        result(i) = result(j)
        result(j) = temp
      end if
    end do
  end do

  ! Output result
  write(*,*) (result(i), i=1,n)

contains

  logical function no_even_digit(val)
    integer :: val
    integer :: digit
    no_even_digit = .true.
    do while (val > 0)
      digit = mod(val, 10)
      if (mod(digit, 2) == 0) then
        no_even_digit = .false.
        return
      end if
      val = val / 10
    end do
  end function no_even_digit

end program main