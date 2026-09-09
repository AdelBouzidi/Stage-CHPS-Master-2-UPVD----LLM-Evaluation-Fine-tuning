program main
  implicit none
  integer, parameter :: max_len = 100
  integer :: x_len
  integer :: x(max_len)
  integer :: result(max_len)
  integer :: n
  integer :: i, j, k
  logical :: has_even_digit

  ! Read input
  read(*,*) x_len
  read(*,*) (x(i), i=1,x_len)

  ! Initialize result array
  n = 0
  do i = 1, x_len
    if (.not. has_even_digit(x(i))) then
      n = n + 1
      result(n) = x(i)
    end if
  end do

  ! Sort result array (simple bubble sort)
  do i = 1, n-1
    do j = i+1, n
      if (result(i) > result(j)) then
        k = result(i)
        result(i) = result(j)
        result(j) = k
      end if
    end do
  end do

  ! Output result
  write(*,*) (result(i), i=1,n)

contains

  logical function has_even_digit(num)
    integer, intent(in) :: num
    integer :: temp
    temp = abs(num)
    do while (temp > 0)
      if (mod(temp, 10) == 0 .or. mod(temp, 10) == 2 .or. mod(temp, 10) == 4 .or. mod(temp, 10) == 6 .or. mod(temp, 10) == 8) then
        has_even_digit = .true.
        return
      end if
      temp = temp / 10
    end do
    has_even_digit = .false.
  end function has_even_digit

end program main