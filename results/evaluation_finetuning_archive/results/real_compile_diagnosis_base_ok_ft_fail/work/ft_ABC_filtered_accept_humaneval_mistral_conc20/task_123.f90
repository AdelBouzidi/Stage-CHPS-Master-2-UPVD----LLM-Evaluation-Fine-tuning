program get_odd_collatz_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer, allocatable :: odd_nums(:)
    
    ! Generate Collatz sequence and collect odd numbers
    odd_nums = []
    temp = n
    do
      if (mod(temp, 2) == 1) then
        odd_nums = [odd_nums, temp]
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    ! Sort the odd numbers
    call sort_array(odd_nums, res)
  end function get_odd_collatz

  subroutine sort_array(arr, sorted_arr)
    implicit none
    integer, intent(in) :: arr(:)
    integer, intent(out) :: sorted_arr(:)
    integer :: i, j, temp
    integer :: n
    
    n = size(arr)
    sorted_arr = arr
    do i = 1, n-1
      do j = i+1, n
        if (sorted_arr(j) < sorted_arr(i)) then
          temp = sorted_arr(i)
          sorted_arr(i) = sorted_arr(j)
          sorted_arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program get_odd_collatz_demo