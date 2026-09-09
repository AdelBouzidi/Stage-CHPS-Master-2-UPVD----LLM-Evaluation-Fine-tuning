program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: result1, result2

  ! Hardcoded input as per example
  numbers_len = 6
  allocate(numbers(numbers_len))
  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 2.2_dp]

  call find_closest_elements(numbers_len, numbers, result1, result2)

  print *, result1, result2

contains

  subroutine find_closest_elements(numbers_len, numbers, result1, result2)
    implicit none
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(numbers_len)
    real(dp), intent(out) :: result1, result2
    integer :: i, j
    real(dp) :: min_diff
    real(dp) :: diff
    integer :: idx1, idx2

    min_diff = huge(min_diff)
    idx1 = 1
    idx2 = 2

    do i = 1, numbers_len - 1
      do j = i + 1, numbers_len
        diff = abs(numbers(i) - numbers(j))
        if (diff < min_diff) then
          min_diff = diff
          idx1 = i
          idx2 = j
        end if
      end do
    end do

    if (numbers(idx1) < numbers(idx2)) then
      result1 = numbers(idx1)
      result2 = numbers(idx2)
    else
      result1 = numbers(idx2)
      result2 = numbers(idx1)
    end if
  end subroutine find_closest_elements

end program find_closest_elements