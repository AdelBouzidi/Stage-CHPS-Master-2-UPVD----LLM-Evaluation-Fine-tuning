program filter_odd_digits
  implicit none
  integer, parameter :: max_len = 100
  integer :: n, i, j, temp
  integer, allocatable :: x(:), result(:)
  integer :: result_len

  ! Read array length
  read(*,*) n

  ! Read array elements
  allocate(x(n))
  read(*,*) x

  ! Filter elements that don't contain any even digit
  result_len = 0
  do i = 1, n
    if (has_only_odd_digits(x(i))) then
      result_len = result_len + 1
    end if
  end do

  ! Allocate result array
  allocate(result(result_len))

  ! Copy filtered elements
  result_len = 0
  do i = 1, n
    if (has_only_odd_digits(x(i))) then
      result_len = result_len + 1
      result(result_len) = x(i)
    end if
  end do

  ! Sort the result array
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
  do i = 1, result_len
    write(*,*) result(i)
  end do

contains

  ! Function to check if a number contains only odd digits
  function has_only_odd_digits(num) result(has_odd)
    implicit none
    integer, intent(in) :: num
    logical :: has_odd
    integer :: digit

    has_odd = .true.
    do while (num > 0)
      digit = mod(num, 10)
      if (digit == 0 .or. digit == 2 .or. digit == 4 .or. digit == 6 .or. digit == 8) then
        has_odd = .false.
        exit
      end if
      num = num / 10
    end do
  end function has_only_odd_digits

end program filter_odd_digits