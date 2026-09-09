program unique_digits_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: x_len
  integer, allocatable :: x(:)
  integer, allocatable :: result(:)
  integer :: i

  ! Hardcoded test case from the example
  x_len = 4
  allocate(x(x_len))
  x = [15, 33, 1422, 1]

  call unique_digits(x_len, x, result)

  print *, 'Result:', result

contains

  subroutine unique_digits(x_len, x, result)
    implicit none
    integer, intent(in) :: x_len
    integer, intent(in) :: x(x_len)
    integer, allocatable, intent(out) :: result(:)
    integer :: i, j, k, n
    integer :: temp
    integer :: digit
    logical :: contains_even_digit

    ! Count how many elements pass the filter
    n = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        n = n + 1
      end if
    end do

    allocate(result(n))
    k = 0
    do i = 1, x_len
      if (.not. contains_even_digit(x(i))) then
        k = k + 1
        result(k) = x(i)
      end if
    end do

    ! Sort the result array in increasing order
    do i = 1, n - 1
      do j = i + 1, n
        if (result(i) > result(j)) then
          temp = result(i)
          result(i) = result(j)
          result(j) = temp
        end if
      end do
    end do

  end subroutine unique_digits

  logical function contains_even_digit(val)
    implicit none
    integer, intent(in) :: val
    integer :: temp, digit
    contains_even_digit = .false.
    do while (val > 0)
      digit = mod(val, 10)
      if (mod(digit, 2) == 0) then
        contains_even_digit = .true.
        return
      end if
      val = val / 10
    end do
  end function contains_even_digit

end program unique_digits_demo