program unique_digits_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i

  ! Hardcoded example input
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  ! Call the function
  result = unique_digits(x_len, x)

  ! Output the result
  print *, 'Result:', result

contains

  function unique_digits(x_len, x) result(res)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable :: res(:)
    integer :: i, j, k, n
    integer :: temp
    integer :: digit
    integer :: contains_even_digit

    ! Count elements that don't contain even digits
    n = 0
    do i = 1, x_len
      contains_even_digit = .false.
      do while (x(i) > 0)
        digit = mod(x(i), 10)
        if (mod(digit, 2) == 0) then
          contains_even_digit = .true.
          exit
        end if
        x(i) = x(i) / 10
      end do
      if (.not. contains_even_digit) then
        n = n + 1
      end if
    end do

    ! Allocate result array with correct size
    allocate(res(n))
    res = 0

    ! Copy elements that don't contain even digits
    k = 1
    do i = 1, x_len
      contains_even_digit = .false.
      do while (x(i) > 0)
        digit = mod(x(i), 10)
        if (mod(digit, 2) == 0) then
          contains_even_digit = .true.
          exit
        end if
        x(i) = x(i) / 10
      end do
      if (.not. contains_even_digit) then
        res(k) = x(i)
        k = k + 1
      end if
    end do

    ! Sort the result array in ascending order
    do i = 1, n - 1
      do j = i + 1, n
        if (res(i) > res(j)) then
          temp = res(i)
          res(i) = res(j)
          res(j) = temp
        end if
      end do
    end do

  end function unique_digits

end program unique_digits_demo