program find_closest_elements_demo
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: result1, result2

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Call the function
  call find_closest_elements(numbers_len, numbers, result1, result2)

  ! Output result
  print *, result1, result2

contains

  subroutine find_closest_elements(int numbers_len, float[] numbers)
    integer, intent(in) :: numbers_len
    real(dp), intent(in) :: numbers(:)
    real(dp), intent(out) :: result1, result2
    integer :: i, j, min_idx, min_j
    real(dp) :: min_diff, diff

    min_diff = huge(0.0_dp)
    min_idx = 0
    min_j = 0

    do i = 1, numbers_len
      do j = i + 1, numbers_len
        diff = abs(numbers(i) - numbers(j))
        if (diff < min_diff) then
          min_diff = diff
          min_idx = i
          min_j = j
        end if
      end do
    end do

    if (numbers(min_idx) < numbers(min_j)) then
      result1 = numbers(min_idx)
      result2 = numbers(min_j)
    else
      result1 = numbers(min_j)
      result2 = numbers(min_idx)
    end if

  end subroutine find_closest_elements

end program find_closest_elements_demo