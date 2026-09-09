program unique_digits
  implicit none
  integer :: x_len
  integer, allocatable :: x(:)
  integer :: result_len
  integer, allocatable :: result(:)
  integer :: i, j, k
  integer :: temp

  ! Read input
  read(*,*) x_len
  allocate(x(x_len))
  read(*,*) x

  ! Process the array
  result_len = 0
  do i = 1, x_len
    if (contains_only_odd_digits(x(i))) then
      result_len = result_len + 1
    end if
  end do

  allocate(result(result_len))
  k = 0
  do i = 1, x_len
    if (contains_only_odd_digits(x(i))) then
      k = k + 1
      result(k) = x(i)
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

contains

  logical function contains_only_odd_digits(n)
    integer, intent(in) :: n
    integer :: digit
    contains_only_odd_digits = .true.
    do while (n > 0)
      digit = mod(n, 10)
      if (mod(digit, 2) == 0) then
        contains_only_odd_digits = .false.
        return
      end if
      n = n / 10
    end do
  end function contains_only_odd_digits

end program unique_digits