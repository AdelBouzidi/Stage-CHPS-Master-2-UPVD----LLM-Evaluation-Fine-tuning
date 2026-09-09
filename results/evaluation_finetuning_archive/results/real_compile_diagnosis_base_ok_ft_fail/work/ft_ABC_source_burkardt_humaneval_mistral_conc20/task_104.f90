program unique_digits
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer :: result_len
  integer, allocatable :: result(:)
  integer :: i, j, temp
  integer :: n, digit
  logical :: even_digit_found

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Process each number
  result_len = 0
  allocate(result(result_len))

  do i = 1, x_len
    n = x(i)
    even_digit_found = .false.
    do while (n > 0)
      digit = mod(n, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        even_digit_found = .true.
        exit
      end if
      n = n / 10
    end do
    if (.not. even_digit_found) then
      result_len = result_len + 1
      allocate(result(result_len))
      result(result_len) = x(i)
    end if
  end do

  ! Sort the result
  do i = 1, result_len - 1
    do j = i + 1, result_len
      if (result(i) > result(j)) then
        temp = result(i)
        result(i) = result(j)
        result(j) = temp
      end if
    end do
  end do

  ! Output the result
  write(*,*) result

end program unique_digits